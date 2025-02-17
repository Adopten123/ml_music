from django import template
import player.views as views
from player import data_for_tests

register = template.Library()

@register.simple_tag
def get_lowermenu():
    return data_for_tests.lowermenu_buttons