from django.shortcuts import render
from apps.repo.models.element.document import Document
from apps.repo.views.index import IndexView


class IndexView(IndexView):
    def get(self, request):
        super().get(request)

        # Fetch additional documents
        recent_documents = Document.objects.all().order_by("-created")[:10]

        # Update the existing context with the new data
        self.context.update({"documents": recent_documents})

        # Render the response with the updated context
        return render(request, self.template_name, context=self.context)
