import logging

from django.conf import settings
from django.db.models import Q

from apps.repo.models.element.document import Document
from apps.repo.utils.static.lookup import get_model

from ..models import DocumentIndex


def get_model_results(type, query, user):  # pragma: no coverage
    Model = get_model(type)
    results = []
    result = Model.objects.filter(
        Q(name__icontains=query)
        | Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(tags__name__icontains=query)
    ).distinct()

    if type == "document":
        for r in result:
            parent_project = r.parent_project
            if not parent_project:
                if r.owner == user:
                    results.append(r)
            else:
                if parent_project.is_member(user):
                    results.append(r)

    elif type == "folder":
        for r in result:
            parent_project = r.parent_project
            if not parent_project:
                if r.owner == user:
                    results.append(r)
            else:
                if parent_project.is_member(user):
                    results.append(r)

    elif type == "project":
        for r in result:
            if r.visibility == "public" or r.visibility == "managed":
                results.append(r)
            elif r.visibility == "private":
                if r.is_member(user):
                    results.append(r)

    return results


def get_fulltext_results(full_text, user):  # pragma: no coverage
    document_ids = DocumentIndex.objects.filter(
        content__icontains=full_text
    ).values_list("document", flat=True)
    result = Document.objects.filter(pk__in=document_ids)

    results = []

    for r in result:
        parent_project = r.parent_project
        if not parent_project:
            if r.owner == user:
                results.append(r)
        else:
            if parent_project.is_member(user):
                results.append(r)

    return results


def remove_duplicate_folders(results):
    # Get folders that are referenced by projects
    project_folders = {r.folder for r in results if r.type == "project"}

    # Remove any folder that is already referenced by a project
    filtered_results = [
        r for r in results if not (r.type == "folder" and r in project_folders)
    ]

    return filtered_results


def pg_search(request):  # pragma: no coverage
    log = logging.getLogger(__name__)
    query = request.GET.get("query", None)
    full_text = request.GET.get("full_text", None)
    types = request.GET.getlist("multi_type", None)

    log.debug(f"Search query: {query}")
    log.debug(f"Full text: {full_text}")
    log.debug(f"Types: {types}")

    results = []
    and_search = "and_search" in types
    types = [t for t in types if t != "and_search"]

    if and_search and query and full_text and settings.ENABLE_FULL_TEXT_SEARCH:
        meta_results = []
        for t in types:
            result = get_model_results(t, query, user=request.user)
            if result:
                meta_results.extend(result)

        text_results = get_fulltext_results(full_text, user=request.user)
        results = list(set(meta_results) & set(text_results))

    else:
        if query and types:
            for t in types:
                result = get_model_results(t, query, user=request.user)
                if result not in results:
                    results.extend(result)

        if full_text and settings.ENABLE_FULL_TEXT_SEARCH:
            result = get_fulltext_results(full_text, user=request.user)
            results.extend(result)

    filtered_results = remove_duplicate_folders(results)

    results = sorted(set(filtered_results), key=lambda r: r.name)
    log.debug(f"Results: {results}")
    return results
