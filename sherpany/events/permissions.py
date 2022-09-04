from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class UserPermissionMixin(LoginRequiredMixin):
    """
    User Permission Mixin to check user is logged in
    and has permission to event.
    """

    def has_permission(self, request):
        event = self.get_object()
        if event and not event.has_edit_permission(request.user):
            return False

        return True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.has_permission(request):
            raise PermissionDenied("You don't have permission to this event.")

        return super().dispatch(request, *args, **kwargs)
