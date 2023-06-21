from django import template

register = template.Library()

@register.filter
def num_range(end):
    return range(1, end+1)


@register.filter
def sector_problems(problems_by_sector, one_start_sector):
    return problems_by_sector[one_start_sector - 1]


@register.filter
def iterate_items(d, item):
    for key, value in d.get(item).items():
        yield key, value


@register.filter
def iterate_displayable_items(d, item, prefix="[display]"):
    for key, value in d.get(item).items():
        if key.startswith(prefix):
            yield key.replace(prefix, ""), value