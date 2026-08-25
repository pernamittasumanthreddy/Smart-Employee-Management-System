from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.permissions.decorators import admin_required
from apps.permissions.models import ModulePermission, Role, SystemModule


@login_required
@admin_required
def role_list(request):
    roles = Role.objects.all().prefetch_related('permissions')
    return render(request, 'permissions/role_list.html', {'roles': roles})

@login_required
@admin_required
def role_matrix(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        for module_choice in SystemModule.choices:
            mod_code = module_choice[0]
            can_create = request.POST.get(f'create_{mod_code}') == 'on'
            can_read = request.POST.get(f'read_{mod_code}') == 'on'
            can_update = request.POST.get(f'update_{mod_code}') == 'on'
            can_delete = request.POST.get(f'delete_{mod_code}') == 'on'
            can_approve = request.POST.get(f'approve_{mod_code}') == 'on'

            ModulePermission.objects.update_or_create(
                role=role,
                module=mod_code,
                defaults={
                    'can_create': can_create,
                    'can_read': can_read,
                    'can_update': can_update,
                    'can_delete': can_delete,
                    'can_approve': can_approve,
                }
            )
        messages.success(request, f"Permission matrix for {role.name} updated successfully.")
        return redirect('permissions:role_list')

    # Load existing permissions map
    existing_perms = {p.module: p for p in role.permissions.all()}
    matrix_data = []
    for mod_code, mod_name in SystemModule.choices:
        perm = existing_perms.get(mod_code)
        matrix_data.append({
            'code': mod_code,
            'name': mod_name,
            'can_create': perm.can_create if perm else False,
            'can_read': perm.can_read if perm else True,
            'can_update': perm.can_update if perm else False,
            'can_delete': perm.can_delete if perm else False,
            'can_approve': perm.can_approve if perm else False,
        })

    return render(request, 'permissions/role_matrix.html', {
        'role': role,
        'matrix_data': matrix_data,
    })
