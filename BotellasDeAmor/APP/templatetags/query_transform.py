from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def query_transform(query_params):
    return urlencode(query_params)