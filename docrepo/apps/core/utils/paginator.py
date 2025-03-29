from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import QuerySet


def get_paginated_objects(
    objects: QuerySet, page: int = 1, paginate_by: int = 10
) -> Page:
    paginator = Paginator(objects, paginate_by)
    page = page

    try:
        paginated_objects = paginator.page(page)  # pragma: no coverage
    except PageNotAnInteger:  # pragma: no coverage
        paginated_objects = paginator.page(1)
    except EmptyPage:  # pragma: no coverage
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects
