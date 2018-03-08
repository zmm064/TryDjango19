from slugify import slugify
from markdown_deux import markdown

from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from .utils import get_read_time


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
    read_time = models.TimeField(null=True, blank=True)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})
        #return "/posts/%s/" % (self.id)

    def get_markdown(self):
        return mark_safe(markdown(self.content))



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    exits = Post.objects.filter(slug=slug)#.exists()
    if exits:
        slug = "%s-%s" % (slug, instance.id) # 暂时还获取不到实例id
    instance.slug = slug

    if instance.content:
        html_string = instance.get_markdown()
        instance.read_time = get_read_time(html_string)

pre_save.connect(pre_save_post_receiver, sender=Post)