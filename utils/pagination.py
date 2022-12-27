from math import ceil

from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    middle_range = ceil(qty_pages/2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)
    
    start_range_off_set = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_off_set

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)
    
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'middle_range': middle_range,
        'start_range': start_range,
        'stop_range': stop_range,
        'page_range': page_range,
        'current_page': current_page,
        'qty_pages': qty_pages,
        'total_pages': total_pages,
        'last_page_out_of_range': stop_range < total_pages,
        'first_page_out_of_range': current_page > middle_range
    }


def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(queryset, per_page)
    paje_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page,
    )
    
    return paje_obj, pagination_range