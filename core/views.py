from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Project, ProjectStatus


@login_required
def dashboard(request):
    projects = Project.objects.select_related('customer', 'salesman').order_by('-updated_at')[:10]
    stats = {
        'total_projects': Project.objects.count(),
        'draft': Project.objects.filter(status=ProjectStatus.DRAFT).count(),
        'quoted': Project.objects.filter(status=ProjectStatus.QUOTED).count(),
        'production': Project.objects.filter(status=ProjectStatus.PRODUCTION).count(),
        'locked': Project.objects.filter(is_locked=True).count(),
    }
    return render(request, 'core/dashboard.html', {
        'recent_projects': projects,
        'stats': stats,
    })


def healthz(request):
    return JsonResponse({'status': 'ok'})
