from django.contrib.auth.forms import AuthenticationForm

class StaffViewAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code = inactive,
            )
