"""
CutFlow – Bar Optimization Engine

Implements first-fit decreasing cutting optimization with kerf, end waste,
profile grouping, and reusable offcut tracking.
"""
from bisect import insort
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import math


@dataclass
class CutRequest:
    profile_id: int
    profile_stock_no: str
    profile_name: str
    length: int
    left_angle: float = 90.0
    right_angle: float = 90.0
    position_code: str = ''
    source_ref: str = ''
    qty: int = 1


@dataclass
class OptimizedCut:
    cut_request: CutRequest
    bar_id: int
    start_pos: int
    end_pos: int


@dataclass
class OptimizedBar:
    bar_id: int
    profile_id: int
    profile_stock_no: str
    profile_name: str
    bar_length: int
    kerf: int = 5
    end_waste: int = 10
    min_reusable: int = 0
    cuts: List[OptimizedCut] = field(default_factory=list)
    source_offcut_id: Optional[int] = None

    @property
    def cut_length_mm(self) -> int:
        return sum(c.cut_request.length for c in self.cuts)

    @property
    def kerf_loss_mm(self) -> int:
        return max(0, (len(self.cuts) - 1) * self.kerf)

    @property
    def reserved_end_waste_mm(self) -> int:
        return self.end_waste if self.cuts else 0

    @property
    def material_consumed_mm(self) -> int:
        return self.cut_length_mm + self.kerf_loss_mm + self.reserved_end_waste_mm

    @property
    def remaining(self) -> int:
        return max(0, self.bar_length - self.material_consumed_mm)

    @property
    def reusable_mm(self) -> int:
        return self.remaining if self.remaining >= self.min_reusable else 0

    @property
    def scrap_mm(self) -> int:
        return self.remaining if self.remaining < self.min_reusable else 0

    @property
    def utilisation_pct(self) -> float:
        if self.bar_length == 0:
            return 0.0
        used = self.cut_length_mm + self.kerf_loss_mm
        return float(round(used / self.bar_length * 100, 2))

    def sort_cuts(self) -> None:
        self.cuts.sort(key=lambda c: c.cut_request.length, reverse=True)
        position = 0
        for index, cut in enumerate(self.cuts):
            cut.start_pos = position
            cut.end_pos = position + cut.cut_request.length
            if index < len(self.cuts) - 1:
                position += cut.cut_request.length + self.kerf


@dataclass
class OptimizationResult:
    profile_id: int
    profile_stock_no: str
    profile_name: str
    bars: List[OptimizedBar] = field(default_factory=list)
    min_reusable: int = 0
    used_offcut_ids: List[int] = field(default_factory=list)
    leftover_offcuts: List[Dict[str, Any]] = field(default_factory=list)
    offcut_scrap_mm: int = 0

    @property
    def total_bars(self) -> int:
        return len(self.bars)

    @property
    def total_bar_length_mm(self) -> int:
        return sum(bar.bar_length for bar in self.bars)

    @property
    def total_used_mm(self) -> int:
        return sum(c.cut_request.length for bar in self.bars for c in bar.cuts)

    @property
    def total_kerf_mm(self) -> int:
        return sum(bar.kerf_loss_mm for bar in self.bars)

    @property
    def total_scrap_mm(self) -> int:
        return sum(bar.scrap_mm for bar in self.bars)

    @property
    def total_offcuts_mm(self) -> int:
        return sum(bar.reusable_mm for bar in self.bars)

    @property
    def total_waste_mm(self) -> int:
        return self.total_scrap_mm

    @property
    def utilisation_pct(self) -> float:
        total_bar_length = self.total_bar_length_mm
        if not total_bar_length:
            return 0.0
        used = self.total_used_mm + self.total_kerf_mm
        return float(round(used / total_bar_length * 100, 2))


def _normalize_offcut_pool(available_offcuts: Optional[List[Any]]) -> Dict[int, List[Dict[str, Any]]]:
    pool: Dict[int, List[Dict[str, Any]]] = {}
    if not available_offcuts:
        return pool
    for candidate in available_offcuts:
        profile_id = getattr(candidate, 'profile_id', None)
        length = getattr(candidate, 'length_mm', None)
        offcut_id = getattr(candidate, 'id', None)
        if length is None:
            length = getattr(candidate, 'length', None)
        if profile_id is None or length is None:
            continue
        try:
            length = int(length)
        except (TypeError, ValueError):
            continue
        if length <= 0:
            continue
        pool.setdefault(profile_id, []).append({
            'offcut_id': offcut_id,
            'length': length,
            'used_cuts': 0,
        })
    for values in pool.values():
        values.sort(key=lambda item: item['length'])
    return pool


class CutsSolver:
    def __init__(self, requests, bar_length, kerf, end_waste, min_reusable, available_offcuts):
        # Sort requests descending by length
        self.requests = sorted(requests, key=lambda r: r.length, reverse=True)
        self.bar_length = bar_length
        self.kerf = kerf
        self.end_waste = end_waste
        self.min_reusable = min_reusable
        self.available_offcuts = available_offcuts  # List of dicts
        
        self.best_bars = None
        self.best_metric = (float('inf'), float('inf'))
        self.time_limit = 0.5  # seconds limit
        self.max_states = 15000
        self.states_visited = 0
        self.start_time = 0.0

    def get_metrics(self, bars):
        standard_bars = 0
        scrap = 0
        for bar in bars:
            if not bar['cuts']:
                continue
            if bar['is_standard']:
                standard_bars += 1
            
            m = len(bar['cuts'])
            rem = bar['bar_length'] - sum(bar['cuts']) - (m - 1) * self.kerf - self.end_waste
            if rem < 0:
                pass
            elif rem < self.min_reusable:
                scrap += rem
        return (standard_bars, scrap)

    def solve(self):
        # 1. Run BFD to get a good initial solution
        self.solve_bfd()
        
        # 2. Run DFS to improve it
        self.start_time = time.time()
        self.states_visited = 0
        
        initial_bars = []
        initial_offcuts = [dict(o) for o in self.available_offcuts]
        
        self._backtrack(0, initial_bars, initial_offcuts)
        return self.best_bars

    def solve_bfd(self):
        bars = []
        offcuts = [dict(o) for o in self.available_offcuts]
        
        for req in self.requests:
            # 1. Try to find the best open bar (Best-Fit)
            best_bar_idx = None
            best_rem = None
            for i, bar in enumerate(bars):
                needed = req.length + (self.kerf if bar['cuts'] else 0)
                if needed <= bar['remaining']:
                    rem_after = bar['remaining'] - needed
                    if best_rem is None or rem_after < best_rem:
                        best_rem = rem_after
                        best_bar_idx = i
                        
            if best_bar_idx is not None:
                bar = bars[best_bar_idx]
                bar['cuts'].append(req.length)
                bar['remaining'] = best_rem
                continue
                
            # 2. Try to find the best offcut (shortest offcut that fits)
            best_offcut_idx = None
            for i, off in enumerate(offcuts):
                if off['used_cuts'] == 0:
                    needed = req.length + self.end_waste
                    if off['length'] >= needed:
                        if best_offcut_idx is None or off['length'] < offcuts[best_offcut_idx]['length']:
                            best_offcut_idx = i
            
            if best_offcut_idx is not None:
                off = offcuts[best_offcut_idx]
                off['used_cuts'] = 1
                new_bar = {
                    'is_standard': False,
                    'bar_length': off['original_length'],
                    'cuts': [req.length],
                    'remaining': off['original_length'] - req.length - self.end_waste,
                    'offcut_id': off['offcut_id']
                }
                bars.append(new_bar)
                continue
                
            # 3. Open a new standard bar
            new_bar = {
                'is_standard': True,
                'bar_length': self.bar_length,
                'cuts': [req.length],
                'remaining': self.bar_length - req.length - self.end_waste,
                'offcut_id': None
            }
            bars.append(new_bar)
            
        self.best_bars = [dict(b, cuts=list(b['cuts'])) for b in bars]
        self.best_metric = self.get_metrics(bars)

    def _backtrack(self, cut_idx, bars, offcuts):
        self.states_visited += 1
        if self.states_visited > self.max_states or (time.time() - self.start_time) > self.time_limit:
            return
            
        # Prune: if we already used more standard bars than the best solution, return
        current_metrics = self.get_metrics(bars)
        if current_metrics[0] > self.best_metric[0]:
            return
            
        if cut_idx == len(self.requests):
            if current_metrics < self.best_metric:
                self.best_metric = current_metrics
                self.best_bars = [dict(b, cuts=list(b['cuts'])) for b in bars]
            return

        req = self.requests[cut_idx]
        
        # Lower bound pruning
        remaining_sum = sum(r.length for r in self.requests[cut_idx:])
        open_rem = sum(b['remaining'] for b in bars)
        current_std_count = sum(1 for b in bars if b['is_standard'])
        if remaining_sum > open_rem:
            min_additional = math.ceil((remaining_sum - open_rem) / self.bar_length)
            if current_std_count + min_additional > self.best_metric[0]:
                return
        
        # Options:
        # 1. Try existing open bars
        seen_rem = set()
        for i, bar in enumerate(bars):
            needed = req.length + (self.kerf if bar['cuts'] else 0)
            if needed <= bar['remaining']:
                key = (bar['is_standard'], bar['remaining'])
                if key in seen_rem:
                    continue
                seen_rem.add(key)
                
                old_cuts = list(bar['cuts'])
                old_rem = bar['remaining']
                
                bar['cuts'].append(req.length)
                bar['remaining'] -= needed
                
                self._backtrack(cut_idx + 1, bars, offcuts)
                
                bar['cuts'] = old_cuts
                bar['remaining'] = old_rem

        # 2. Try unused offcuts
        seen_offcut_len = set()
        for i, off in enumerate(offcuts):
            if off['used_cuts'] == 0:
                needed = req.length + self.end_waste
                if off['length'] >= needed:
                    if off['length'] in seen_offcut_len:
                        continue
                    seen_offcut_len.add(off['length'])
                    
                    off['used_cuts'] = 1
                    new_bar = {
                        'is_standard': False,
                        'bar_length': off['original_length'],
                        'cuts': [req.length],
                        'remaining': off['original_length'] - req.length - self.end_waste,
                        'offcut_id': off['offcut_id']
                    }
                    bars.append(new_bar)
                    
                    self._backtrack(cut_idx + 1, bars, offcuts)
                    
                    bars.pop()
                    off['used_cuts'] = 0

        # 3. Try a new standard bar (only if we don't exceed the best standard bars)
        if current_std_count < self.best_metric[0]:
            new_bar = {
                'is_standard': True,
                'bar_length': self.bar_length,
                'cuts': [req.length],
                'remaining': self.bar_length - req.length - self.end_waste,
                'offcut_id': None
            }
            bars.append(new_bar)
            
            self._backtrack(cut_idx + 1, bars, offcuts)
            
            bars.pop()


def optimize_cuts(
    cut_requests: List[CutRequest],
    bar_length: int = 6000,
    kerf: int = 5,
    end_waste: int = 10,
    min_reusable: int = 300,
    available_offcuts: Optional[List[Any]] = None,
) -> Dict[int, OptimizationResult]:
    profile_groups: Dict[int, List[CutRequest]] = {}
    for request in cut_requests:
        profile_groups.setdefault(request.profile_id, []).append(request)

    offcut_pool = _normalize_offcut_pool(available_offcuts)
    results: Dict[int, OptimizationResult] = {}

    for profile_id, requests in profile_groups.items():
        expanded: List[CutRequest] = []
        for request in requests:
            quantity = max(1, int(request.qty))
            for _ in range(quantity):
                expanded.append(request)

        if not expanded:
            continue

        for req in expanded:
            if req.length > bar_length - end_waste:
                raise ValueError(
                    f"Cut length {req.length}mm exceeds available bar capacity "
                    f"{bar_length - end_waste}mm for profile {req.profile_stock_no}."
                )

        profile_offcuts = offcut_pool.get(profile_id, [])
        for off in profile_offcuts:
            off['original_length'] = off['length']

        sample = expanded[0]
        profile_stock_no = sample.profile_stock_no
        profile_name = sample.profile_name

        solver = CutsSolver(
            requests=expanded,
            bar_length=bar_length,
            kerf=kerf,
            end_waste=end_waste,
            min_reusable=min_reusable,
            available_offcuts=profile_offcuts
        )
        best_bars = solver.solve()

        # Re-associate cuts with CutRequest objects
        req_pool = {}
        for req in expanded:
            req_pool.setdefault(req.length, []).append(req)

        bars_result = []
        used_offcut_ids = []
        leftover_offcuts = []
        offcut_scrap_mm = 0

        next_bar_id = 1
        for bar in best_bars:
            bar_cuts = []
            for length in bar['cuts']:
                req = req_pool[length].pop(0)
                bar_cuts.append(OptimizedCut(
                    cut_request=req,
                    bar_id=next_bar_id,
                    start_pos=0,
                    end_pos=req.length,
                ))

            opt_bar = OptimizedBar(
                bar_id=next_bar_id,
                profile_id=profile_id,
                profile_stock_no=profile_stock_no,
                profile_name=profile_name,
                bar_length=bar['bar_length'],
                kerf=kerf,
                end_waste=end_waste,
                min_reusable=min_reusable,
                cuts=bar_cuts,
                source_offcut_id=bar['offcut_id'],
            )
            opt_bar.sort_cuts()
            bars_result.append(opt_bar)
            next_bar_id += 1

            if bar['offcut_id'] is not None:
                used_offcut_ids.append(bar['offcut_id'])
                rem = opt_bar.remaining
                if rem >= min_reusable:
                    leftover_offcuts.append({
                        'offcut_id': bar['offcut_id'],
                        'profile_id': profile_id,
                        'length': rem,
                    })
                else:
                    offcut_scrap_mm += rem

        results[profile_id] = OptimizationResult(
            profile_id=profile_id,
            profile_stock_no=profile_stock_no,
            profile_name=profile_name,
            bars=bars_result,
            min_reusable=min_reusable,
            used_offcut_ids=used_offcut_ids,
            leftover_offcuts=leftover_offcuts,
            offcut_scrap_mm=offcut_scrap_mm,
        )

    return results
