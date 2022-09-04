from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from events.forms import EventForm
from events.models import Event, EventRSVP
from events.permissions import UserPermissionMixin


class BaseEventQueryMixin:
    queryset = Event.objects.select_related("creator").prefetch_related("participants")


class MyEventView(
    LoginRequiredMixin,
    BaseEventQueryMixin,
    ListView,
):
    """My event view."""

    model = Event
    template_name = "events/my_events.html"
    paginate_by = 10

    def get_queryset(self):
        """Override to filter queryset by logged in user."""
        queryset = super().get_queryset()
        return queryset.filter(creator=self.request.user)


class CreateUpdateEventView(
    UserPermissionMixin,
    SuccessMessageMixin,
    BaseEventQueryMixin,
    CreateView,
    UpdateView,
):
    "Create and update event view."
    form_class = EventForm
    template_name = "events/create_event.html"
    success_url = reverse_lazy("events:my_events")
    success_message = _("Event has been saved")

    def get_object(self, queryset=None):
        """Override to to support create and update."""
        try:
            return super(CreateUpdateEventView, self).get_object(queryset)
        except AttributeError:
            return None

    def form_valid(self, form):
        """Override to set creator as logged in user."""
        form.instance.creator = self.request.user
        return super().form_valid(form)


class DeleteEventView(
    UserPermissionMixin,
    BaseEventQueryMixin,
    DeleteView,
):
    "Delete event view."
    success_url = reverse_lazy("events:my_events")
    success_message = _("Event has been deleted")

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(*args, **kwargs)


class DetailEventView(
    LoginRequiredMixin,
    BaseEventQueryMixin,
    DetailView,
):
    """Detail event view."""

    template_name = "events/detail_event.html"

    def get_context_data(self, **kwargs):
        """Override get_context_data to add is_participant flag."""
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context.update(
            {
                "is_participant": instance.is_participant(self.request.user),
            }
        )
        return context


class PublicEventView(
    LoginRequiredMixin,
    BaseEventQueryMixin,
    ListView,
):
    """Public event view."""

    template_name = "events/public_events.html"
    paginate_by = 10


class ReserveEventView(
    LoginRequiredMixin,
    BaseEventQueryMixin,
    CreateView,
):
    """Reserve event view."""

    success_url = reverse_lazy("events:public_events")
    success_message = _("You have successfully reserved to the event")

    def post(self, request, pk):
        event = get_object_or_404(
            self.get_queryset(),
            id=pk,
        )
        if event.is_passed():
            messages.error(request, _("You can't do reservation to passed event."))

        elif event.is_owner(request.user):
            messages.error(request, _("You can't do reservation to your own event."))

        elif event.is_participant(request.user):
            messages.error(request, _("You already reserved this event."))

        else:
            EventRSVP.objects.create(user=request.user, event=event)
            messages.success(request, self.success_message)

        return redirect(self.success_url)


class WithdrawReservationEventView(
    LoginRequiredMixin,
    BaseEventQueryMixin,
    DeleteView,
):
    """Withdraw reservation event view."""

    success_url = reverse_lazy("events:public_events")
    success_message = _("You have successfully withdraw reservation to the event")

    def delete(self, *args, **kwargs):
        event = self.get_object()
        if not event.is_participant(self.request.user):
            return HttpResponseForbidden()

        event.participants.get(user=self.request.user).delete()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
