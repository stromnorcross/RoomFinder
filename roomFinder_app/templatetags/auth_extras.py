from django import template
from django.contrib.auth.models import Group 

# * REFERENCES
# * Title: sw-django-utils, get_value_from_dict
# * Author: Sergey Telminov
# * Date: May 6, 2016
# * URL: https://github.com/telminov/sw-django-utils/blob/master/djutils/templatetags/djutils.py
# * Software License: N/A

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    if key:
        return dict_data.get(key)
