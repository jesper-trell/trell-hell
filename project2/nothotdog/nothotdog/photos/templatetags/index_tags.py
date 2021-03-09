from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, query_field, value):
    query_dict = context['request'].GET.copy()
    query_dict[query_field] = value
    return query_dict.urlencode()
