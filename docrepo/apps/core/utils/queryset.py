def is_reversed(order_by_filter: str) -> bool:  # pragma: no coverage
    return order_by_filter.startswith("-")


def field_name(order_by_filter: str) -> str:  # pragma: no coverage
    return order_by_filter.lstrip("-")
