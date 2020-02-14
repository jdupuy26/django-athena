from django import template

register = template.Library()

@register.simple_tag
def call_function(obj, method_name):
    method = getattr(obj, method_name)
    return method

