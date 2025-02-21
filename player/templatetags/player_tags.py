"""Player tags file"""
from django import template
from player import data_for_tests

register = template.Library()

@register.simple_tag
def get_lowermenu():
    """Getting lower_menu"""
    return data_for_tests.lowermenu_buttons
