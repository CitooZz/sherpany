from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import RegisterUserForm


class RegisterView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"
