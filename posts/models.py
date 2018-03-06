from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.conf import settings
from slugify import slugify

# Create your models here.

def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)

class Post(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title     = models.CharField(max_length=120)
    slug      = models.SlugField(unique=True)
    image     = models.FileField(null=True, blank=True, upload_to=upload_location)
    content   = models.TextField()
    draft     = models.BooleanField(default=False)
    publish   = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})
        #return "/posts/%s/" % (self.id)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    exits = Post.objects.filter(slug=slug)#.exists()
    if exits:
        slug = "%s-%s" % (slug, instance.id) # 暂时还获取不到实例id
    instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Post)