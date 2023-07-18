import re
import copy
from django.template import Library
from django.conf import settings

register = Library()


@register.simple_tag
def un_deploy_num(env_object):
    total = env_object.deploytask_set.all().count()
    un_deploy = env_object.deploytask_set.filter(status=1).count()
    msg = "%s/%s" % (un_deploy, total)
    return msg


@register.inclusion_tag('web/include/menu.html')
def menu(request):
    menu_list = copy.deepcopy(settings.HG_MENU_LIST)
    for row in menu_list:
        if re.match(row['match'], request.path_info):
            row['class'] = "active"
            break

    return {'menu_list': menu_list}
