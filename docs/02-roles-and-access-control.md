# Roles and Access Control

## Role Model

User roles are stored in `accounts.UserProfile.role`.

| Role | Intended Responsibility |
| --- | --- |
| `admin` | Full control over setup, catalog, users, project locking, and Django admin. |
| `salesman` | Customer, project, measurement, and quotation workflow. |
| `production` | Production job, cut list, optimization, hardware, glass, and offcut workflow. |
| `viewer` | Read-only business visibility. |

## Current Enforcement Pattern

The project contains:

- `core.decorators.role_required`: role gate for selected views.
- `core.middleware.RoleMiddleware`: adds `request.user_role` for templates.
- Django authentication: protects login-required views.
- Django admin: available at `/admin/`.

## Commercial Access Rules

Before commercial deployment, every URL should have an explicit access decision.

| Area | Admin | Salesman | Production | Viewer |
| --- | --- | --- | --- | --- |
| Dashboard | Full | Own/team view | Production view | Read-only |
| Customers | Full | Create/edit assigned | Read-only if needed | Read-only |
| Projects | Full | Create/edit until locked | Read after production starts | Read-only |
| Measurements | Full | Create/edit until locked | Read/use for job generation | Read-only |
| Quotations | Full | Create/revise/send | Read accepted production quotes | Read-only |
| Catalog | Full | Read | Read | Read |
| Company settings | Full | No | No | No |
| Production jobs | Full | Read | Create/update/optimize | Read-only |
| Offcuts | Full | No | Create/update/use | Read-only |
| Django admin | Full | No | No | No |

## Account Lifecycle

1. Admin creates the Django user.
2. Admin creates or verifies the related user profile.
3. Admin assigns the role.
4. Admin verifies the user can log in and access only the expected screens.
5. Inactive employees should have both `User.is_active=False` and `UserProfile.is_active=False`.

## Commercial Controls to Add or Verify

- Require strong production passwords.
- Configure password reset email for production.
- Restrict `/admin/` to admin users and preferably trusted networks.
- Add explicit role checks to all create/edit/delete/optimize/download actions.
- Add audit log writes for high-value actions: quotation status changes, project lock/unlock, production generation, optimization, catalog changes, and settings changes.
- Review all templates so hidden buttons are not the only access control.
- Confirm inactive profiles cannot access operational screens.

