from django.contrib.admin import AdminSite
from casetool.staffviewauthenticationform import StaffViewAuthenticationForm

# define non-root admin site
class StaffView(AdminSite):
    site_header = 'OSCMT staff view'
    login_form = StaffViewAuthenticationForm

    def has_permission(self, request):
        return request.user.is_active


admin_site = StaffView(name='staffview')
