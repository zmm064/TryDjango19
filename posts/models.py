from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)

class Post(models.Model):
    title     = models.CharField(max_length=120)
    image     = models.FileField(null=True, blank=True, upload_to=upload_location)
    content   = models.TextField()
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'id': self.id})
        #return "/posts/%s/" % (self.id)