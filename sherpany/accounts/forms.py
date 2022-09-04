from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class RegisterUserForm(UserCreationForm):
    """Override UserCreationForm to use email."""

    class Meta:
        model = User
        fields = ("email",)

    def save(self, commit=True):
        """Override save method to set username as email."""
        user = super().save(commit=False)
        user.username = self.cleaned_data.get("email")
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()

        return user
