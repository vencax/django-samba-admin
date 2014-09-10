from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.views.decorators.cache import never_cache

from nss_admin.models import SysUser, SysMembership, SysGroup

from .models import ShareConnection


osMapping = {
    'Windows_NT': 'xp'
}

# this allow to add another OS mapping without modifying this source
customOsMapping = getattr(settings, 'CUSTOM_OS_MAPPING', {})
osMapping.update(customOsMapping)

printersMapping = getattr(settings, 'SAMB_PRINTERS_MAPPING', {})
shareServer = getattr(settings, 'SHARE_SERVER', 'lserver')


@never_cache
def logonScript(request, username, os):
    """
    Prepares logon script based on user and operating sys.
    """
    try:
        u = SysUser.objects.get(user_name=username)
        sharesToMount = _getSharesToMount(u)
        printersToMount = _getPrintersToMount(u)
        userGroups = [group.group_name for group in _getUserGroups(u)]

        template = 'samba_admin/%s.html' % osMapping[os]

        script = loader.render_to_string(template, {
            'sharesToMount': sharesToMount,
            'printersToMount': printersToMount,
            'shareServer': shareServer,
            'userGroups': userGroups,
        }, RequestContext(request))

        # make f*cking M$ endlines
        script = script.replace('\n', '\r\n')
    except Exception:
        script = ''

    return HttpResponse(script)

# ------------------------------ privates ------------------------------------


def _getUserGroups(user):
    uMships = SysMembership.objects.filter(user=user)
    uMships = uMships.values_list('group_id', flat=True)
    userGroups = SysGroup.objects.filter(group_id__in=uMships)
    return tuple(userGroups) + (user.gid, )


def _getSharesToMount(user):
    shrs = ShareConnection.objects.filter(groups__in=_getUserGroups(user))
    return shrs.distinct()


def _getPrintersToMount(user):
    printersToMount = []
    for g in user.sysgroup_set.all():
        for printer, allowedGroups in printersMapping.items():
            if g.group_name.lower() in allowedGroups:
                printersToMount.append(printer)
    return printersToMount

# ------------------------------ EOF ------------------------------------------
