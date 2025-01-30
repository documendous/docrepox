from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.comments.utils import get_details_url
from apps.core.views import View
from apps.repo import rules
from apps.repo.utils.static.lookup import get_model

from .models import Comment


class AddCommentView(View):
    def post(self, request, element_type, element_id):
        """
        View to add comments for a commentable element
        """
        Model = get_model(element_type)
        instance = Model.objects.get(pk=element_id)
        rules.can_add_comment(request, instance)

        user = request.user
        content = request.POST.get("content", None)

        if content:
            instance.comments.add(Comment.objects.create(author=user, content=content))
            instance.save()

        self.context.update({"element": instance})

        return render(request, "comments/partials/_comment_list.html", self.context)


class DeleteCommentView(View):
    """
    View to delete comments for a commentable element
    """

    def post(self, request, element_type, element_id, comment_id):
        rules.can_delete_comment(request, comment_id, element_type, element_id)
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        url = get_details_url(element_type=element_type, element_id=element_id)
        return HttpResponseRedirect(url + "#comments")
