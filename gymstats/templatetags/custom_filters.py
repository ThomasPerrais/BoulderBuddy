from django import template

register = template.Library()


@register.filter
def achievement(problems, problem):
    return problems[problem]["achievement"]

@register.filter
def attempts(problems, problem):
    return problems[problem]["attempts"]


@register.filter
def section_problems(problems, section):
    key, value = __parse_section(section)
    return [pb for pb in problems.keys() if __is_match(pb, key, value)]


@register.filter
def section_has_problems(problems, section):
    key, value = __parse_section(section)
    for pb in problems.keys():
        if __is_match(pb, key, value):
            return True
    return False


def __parse_section(section):
    key = "@default"
    value = section
    if section.startswith('s:'):
        value = int(section[2:])
        key = "by-sector"
    elif section.startswith('g:'):
        value = section[2:]
        key = "by-grade"
    return key, value


def __is_match(problem, key, value):
    if key == "by-sector" and problem.sector.sector_id == value:
        return True
    elif key == "by-grade" and problem.grade == value:
        return True
    return False


@register.filter
def iterate_items(d, item):
    for key, value in d.get(item).items():
        yield key, value


@register.filter
def iterate_displayable_items(d, item, prefix="[display]"):
    for key, value in d.get(item).items():
        if key.startswith(prefix):
            yield key.replace(prefix, ""), value