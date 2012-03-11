from django.template import RequestContext
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from nss_admin.models import SysUser

sharesMapping = getattr(settings, 'SAMB_SHARES_MAPPING', {})
printersMapping = getattr(settings, 'SAMB_PRINTERS_MAPPING', {})

osMapping = {
    'Windows_NT' : 'xp'
}

# this allow to add another OS mapping without modifying this source
customOsMapping = getattr(settings, 'CUSTOM_OS_MAPPING', {})
osMapping.update(customOsMapping)

def logonScript(request, username, os):
    """
    Prepares logon script based on user and operating sys.
    """
    try:
        u = SysUser.objects.get(user_name=username)
        sharesToMount = _getSharesToMount(u)        
        printersToMount = _getPrintersToMount(u)
        
        shareServer = 'SERVER'
        template = 'samba_admin/%s.html' % osMapping[os]
        
        script = loader.render_to_string(template, {
            'sharesToMount' : sharesToMount,
            'printersToMount' : printersToMount,
            'shareServer' : shareServer
        }, RequestContext(request))
        
        # make f*cking M$ endlines
        script = script.replace('\n', '\r\n')
    except Exception:
        script = ''
    
    return HttpResponse(script)
  
# ------------------------------ privates ------------------------------------

def _pooky(g): return g.group_name.lower()
  
def _getSharesToMount(user):
    sharesToMount = {}
    for g in user.sysgroup_set.all():
        if _pooky(g) in sharesMapping:
            info = sharesMapping[_pooky(g)]
            sharesToMount[info[0]] = info[1]
    return sharesToMount
  
def _getPrintersToMount(user):
    printersToMount = []
    for g in user.sysgroup_set.all():
        for printer, allowedGroups in printersMapping.items():
            if _pooky(g) in allowedGroups:
                printersToMount.append(printer)
    return printersToMount
  
# ------------------------------ EOF ------------------------------------------