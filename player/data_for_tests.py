

lowermenu_buttons = [
    {'name': 'Legal', 'url': 'legal'},
    {'name': 'Safety & Privacy', 'url': 'safety_and_privacy'},
    {'name': 'Privacy Policy', 'url': 'privacy_policy'},
    {'name': 'Cookies', 'url': 'cookies'},
    {'name': 'About Ads', 'url': 'about_ads'},
    {'name': 'Accessibility', 'url': 'accessibility'},
]

#При помощи url в словаре lower_buttons ищет name
def get_title_by_infoslug(info_slug):
    return next((item['name'] for item in lowermenu_buttons if item['url'] == info_slug), None)