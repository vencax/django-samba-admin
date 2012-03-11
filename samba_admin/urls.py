from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<username>[0-9A-Za-z_]{1,})/(?P<os>[0-9A-Za-z_]{1,})/logon.bat$', 
        views.logonScript, name='samba_admin_logonscript'),
)