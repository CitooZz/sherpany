from django.urls import path

from events.views import (
    CreateUpdateEventView,
    DeleteEventView,
    DetailEventView,
    MyEventView,
    PublicEventView,
    ReserveEventView,
    WithdrawReservationEventView,
)

app_name = "event"

urlpatterns = [
    path("", MyEventView.as_view(), name="my_events"),
    path("create/", CreateUpdateEventView.as_view(), name="create_event"),
    path(
        "<int:pk>/",
        DetailEventView.as_view(),
        name="detail_event",
    ),
    path(
        "<int:pk>/update/",
        CreateUpdateEventView.as_view(),
        name="update_event",
    ),
    path("<int:pk>/delete/", DeleteEventView.as_view(), name="delete_event"),
    path("public/", PublicEventView.as_view(), name="public_events"),
    path(
        "<int:pk>/reserve/",
        ReserveEventView.as_view(),
        name="reserve_event",
    ),
    path(
        "<int:pk>/withdraw-reservation/",
        WithdrawReservationEventView.as_view(),
        name="withdraw_event_reservation",
    ),
]
