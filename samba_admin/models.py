from django.db import models
from django.utils.translation import ugettext_lazy as _

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