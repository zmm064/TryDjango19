from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from posts.models import Post
# Create your models here.
class Comment(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    post      = models.ForeignKey(Post)
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent    = models.ForeignKey("self", null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True