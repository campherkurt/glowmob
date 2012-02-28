from django import template
register = template.Library()

@register.simple_tag
def comment_number(count, counter, current_page, items_per_page):
    return count - ((current_page - 1) * items_per_page) - counter