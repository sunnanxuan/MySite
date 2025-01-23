from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """返回字典中对应键的值"""
    return dictionary.get(key)