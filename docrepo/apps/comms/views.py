from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.core.views import View
from apps.repo.utils.system.object import get_system_root_folder

from .models import Communication


class CommListView(View):
    read_order_by_filter, unread_order_by_filter = ("-created", "-created")

    def _set_filters(self) -> None:  # pragma: no coverage
        order_by_filter = self.request.GET.get("order_by", None)
        filter_condition = self.request.GET.get("condition", None)

        if filter_condition and order_by_filter:
            if filter_condition == "read":
                self.read_order_by_filter = order_by_filter
            elif filter_condition == "unread":
                self.unread_order_by_filter = order_by_filter

    def _get_comms(self) -> tuple:
        self._set_filters()

        read_comms = Communication.objects.filter(
            msg_to=self.request.user, acknowledged=True
        ).order_by(self.read_order_by_filter)

        unread_comms = Communication.objects.filter(
            msg_to=self.request.user, acknowledged=False
        ).order_by(self.unread_order_by_filter)

        return (read_comms, unread_comms)

    def get(self, request):
        read_comms, unread_comms = self._get_comms()

        return render(
            request,
            "comms/comm_list.html",
            {
                "read_comms": read_comms,
                "unread_comms": unread_comms,
                "home_folder_id": request.user.profile.home_folder.id,
                "root_folder_id": get_system_root_folder().id,
            },
        )


class AcknowledgeCommView(View):
    def post(self, request, comm_id):  # pragma: no coverage
        comm = Communication.objects.get(pk=comm_id)
        comm.set_acknowledged()
        return HttpResponseRedirect(reverse("repo:comms:comm_list"))


class DeleteCommView(View):
    def post(self, request, comm_id):  # pragma: no coverage
        comm = Communication.objects.get(pk=comm_id)
        comm.delete()
        return HttpResponseRedirect(reverse("repo:comms:comm_list"))
