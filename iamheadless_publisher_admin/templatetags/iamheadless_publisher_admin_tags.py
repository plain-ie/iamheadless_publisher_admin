import datetime

from django import template
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from ..conf import settings
from .. import utils


register = template.Library()


@register.simple_tag
def build_id():
    build_id = getattr(settings, 'BUILD_ID', None)
    if build_id is None:
        build_id = datetime.datetime.now().strftime('%Y%m%d%H')
    return build_id


@register.simple_tag
def define(value):
    return value


@register.filter(name='extend_field_css_classes')
def extend_field_css_classes(field, classes):
    cls = field.field.widget.attrs.get('class', '')
    field.field.widget.attrs['class'] = cls + ' ' + classes
    return field


@register.inclusion_tag('iamheadless_publisher_admin/components/navbar/footer.html', takes_context=True)
def footer(context):
    request = context['request']
    return {
        'request': request
    }


@register.inclusion_tag('iamheadless_publisher_admin/components/navbar/main_menu.html', takes_context=True)
def main_menu(context):

    request = context['request']
    user = utils.get_request_user(request)
    project_id = utils.get_request_project_id(request)

    links = []

    if user.is_authenticated is True:
        links += [
            {
                'title': _('Items'),
                'url': reverse(settings.URLNAME_ITEMS, kwargs={'project_id': project_id}),
                'links': None,
            },
            {
                'title': user.email,
                'url': None,
                'links': [
                    {
                        'title': _('Sign out'),
                        'url': reverse(settings.URLNAME_SIGN_OUT),
                    }
                ],
            }
        ]

    if user.is_authenticated is False:
        links += [
            {
                'title': _('Sign in'),
                'url': reverse(settings.URLNAME_SIGN_IN),
                'links': None,
            }
        ]

    return {
        'brand_image': None,
        'brand_link': '/',
        'brand_title': settings.PROJECT_TITLE,
        'links': links,
        'request': request,
    }


@register.filter(name='override_disabled_state')
def override_disabled_state(field, disabled):
    field.field.widget.attrs['disabled'] = disabled
    return field


@register.filter(name='override_field_attr')
def override_field_attr(field, value):
    attr_name, attr_value = value.split('|')
    field.field.widget.attrs[attr_name] = attr_value
    return field


@register.simple_tag
def project_title():
    return getattr(settings, 'PROJECT_TITLE')


@register.simple_tag
def setting(name):
    return getattr(settings, name)
