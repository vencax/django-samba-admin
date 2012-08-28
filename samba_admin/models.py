from django.db import models
from django.utils.translation import ugettext_lazy as _
from nss_admin.models import SysGroup
import string

letterOpts = ((l, l) for l in string.ascii_uppercase)

class ShareConnection(models.Model):
    server = models.CharField(verbose_name=_('server'), max_length=16,
                              help_text=_('either IP address or name'))
    path = models.CharField(verbose_name=_('path'), max_length=32)
    letter = models.CharField(verbose_name=_('letter'), max_length=1, unique=True,
                              choices=letterOpts)
    user = models.CharField(verbose_name=_('user'), max_length=16, blank=True)
    passwd = models.CharField(verbose_name=_('passwd'), max_length=16, blank=True)
    groups = models.ManyToManyField(SysGroup)

    class Meta:
        verbose_name = _('share connection')
        verbose_name_plural = _('share connections')

    def __unicode__(self):
        return '%s: \\%s\%s' % (self.letter, self.server, self.path)

class SambaShare(models.Model):
    """
    Represent a samba share.
    """
    name = models.CharField(verbose_name=_('name'), max_length=32, unique=True,
                            primary_key=True)
    path = models.CharField(verbose_name=_('path'), max_length=32)

    class Meta:
        abstract = True
# -----------------------------------------------------------------------------
