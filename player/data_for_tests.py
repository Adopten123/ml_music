""" module with debug functions """
from django.core.paginator import Paginator

lowermenu_buttons = [
    {'name': 'Legal', 'url': 'legal'},
    {'name': 'Safety & Privacy', 'url': 'safety_and_privacy'},
    {'name': 'Privacy Policy', 'url': 'privacy_policy'},
    {'name': 'Cookies', 'url': 'cookies'},
    {'name': 'About Ads', 'url': 'about_ads'},
    {'name': 'Accessibility', 'url': 'accessibility'},
]

def get_title_by_infoslug(info_slug):
    """ При помощи url в словаре lower_buttons ищет name"""
    return next((item['name'] for item in lowermenu_buttons if item['url'] == info_slug), None)

def get_page_obj(request, tracks):
    """Getting tracks for player"""
    paginator = Paginator(tracks, 1)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
