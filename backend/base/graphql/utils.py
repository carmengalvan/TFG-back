from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from base.models import OrderingChoice

from .types import PageInfoType

MAX_PAGE_SIZE = 100


def get_paginator(
    qs,
    page_size: int | None,
    page: int | None,
    order_by,
    paginated_type,
    **kwargs,
):
    page_size = page_size or 10
    page = page or 1

    p = Paginator(qs, min(MAX_PAGE_SIZE, page_size))
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    page_info = PageInfoType(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        total_results=p.count,
        order_by=order_by,
    )
    return paginated_type(
        page_info=page_info,
        edges=page_obj.object_list,
        **kwargs,
    )


def order_queryset(query, order_by):
    order = []

    for item in order_by:
        field = item.field
        ordering = item.ordering
        order.append(
            "{}{}".format("" if ordering == OrderingChoice.ASC else "-", field)
        )
    query = query.order_by(*order)

    return query
