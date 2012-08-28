from django.template import RequestContext
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from nss_admin.models import SysUser, SysMembership

from .models import ShareConnection

osMapping = {
    'Windows_NT' : 'xp'
}

# this allow to add another OS mapping without modifying this source
customOsMapping = getattr(settings, 'CUSTOM_OS_MAPPING', {})
osMapping.update(customOsMapping)

printersMapping = getattr(settings, 'SAMB_PRINTERS_MAPPING', {})
homesServer = getattr(settings, 'HOMES_SERVER', 'lserver')

def logonScript(request, username, os):
    """
    Prepares logon script based on user and operating sys.
    """
    try:
        u = SysUser.objects.get(user_name=username)
        sharesToMount = _getSharesToMount(u)
        printersToMount = _getPrintersToMount(u)
        
        template = 'samba_admin/%s.html' % osMapping[os]
        
        script = loader.render_to_string(template, {
            'sharesToMount' : sharesToMount,
            'printersToMount' : printersToMount,
            'homesServer' : homesServer,
        }, RequestContext(request))
        
        # make f*cking M$ endlines
        script = script.replace('\n', '\r\n')
    except Exception:
        script = ''
    
    return HttpResponse(script)
  
# ------------------------------ privates ------------------------------------
  
def _getSharesToMount(user):
    userGroups = SysMembership.objects.filter(user=user)
    userGroups = tuple(userGroups) + (user.gid, )
    return ShareConnection.objects.filter(groups__in=userGroups)
  
def _getPrintersToMount(user):
    printersToMount = []
    for g in user.sysgroup_set.all():
        for printer, allowedGroups in printersMapping.items():
            if g.group_name.lower() in allowedGroups:
                printersToMount.append(printer)
    return printersToMount
  
# ------------------------------ EOF ------------------------------------------