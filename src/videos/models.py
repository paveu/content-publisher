from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, \
                                                GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from accounts.models import MyUser

from .utils import get_vid_for_direction


class VideoQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def has_embed(self):
        return self.filter(embed_code__isnull=False).exclude(
            embed_code__exact=""
            )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def get_featured(self):
        return self.get_queryset().active().featured()

    def all(self):
        return self.get_queryset().active().has_embed()


class Video(models.Model):
    user = models.ForeignKey(MyUser)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    embed_code = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    order = models.PositiveIntegerField(default=1)
    # https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/
    # TaggedItem(models.Model)
    tags = GenericRelation("TaggedItem", null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    free_preview = models.BooleanField(default=False)
    category = models.ForeignKey("Category", default=1)
    timestamp = models.DateTimeField(auto_now_add=True,
                                     auto_now=False,
                                     null=True)
    updated = models.DateTimeField(auto_now_add=False,
                                   auto_now=True,
                                   null=True)

    objects = VideoManager()

    class Meta:
        unique_together = ('slug', 'category')
        ordering = ['order', '-timestamp']
        verbose_name_plural = "Videos"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={"vid_slug": self.slug,
                                               "cat_slug": self.category.slug})

    def get_share_link(self):
        full_url = "%s%s" % (settings.FULL_DOMAIN_NAME,
                             self.get_absolute_url())
        return full_url

    def get_next_url(self):
        video = get_vid_for_direction(self, "next")
        if video is not None:
            return video.get_absolute_url()
        return None

    def get_previous_url(self):
        video = get_vid_for_direction(self, "previous")
        if video is not None:
            return video.get_absolute_url()
        return None

    @property
    def has_preview(self):
        if self.free_preview:
            return True
        return False

    def get_image_url(self):
        return "%s%s" % (settings.MEDIA_URL, self.image)


def video_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    Automatically create a slug for newly created Video
    """
    if created:
        slug_title = slugify(instance.title)
        new_slug = "%s %s %s" % (instance.title,
                                 instance.category.slug,
                                 instance.id)
        try:
            instance.slug = slugify(new_slug)
            instance.save()
            print "model exists, new slug generated"
        except Video.DoesNotExist:
            instance.slug = slug_title
            instance.save()
            print "slug and model created"
        except Video.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
            instance.save()
            print "multiple models exists, new slug generated"
        except:
            pass

post_save.connect(receiver=video_post_save_receiver, sender=Video)


class CategoryQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def get_featured(self):
        return self.get_queryset().active().featured()

    def all(self):
        return self.get_queryset().active()


class Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=5000, null=True, blank=True)
    # TaggedItem(models.Model):
    tags = GenericRelation("TaggedItem", null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(default='abc', unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = CategoryManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cat_detail", kwargs={"cat_slug": self.slug})

    def get_image_url(self):
        return "%s%s" % (settings.MEDIA_URL, self.image)

    class Meta:
        verbose_name_plural = "Categories"

TAG_CHOICES = (
    ("python", "python"),
    ("django", "django"),
    ("css", "css"),
    ("bootstrap", "bootstrap"),
    ("music", "music"),
)


class TaggedItem(models.Model):
    """
    It allows to bind specific model with a tag.
    Additional configuration in admin file is needed
    """
    tag = models.SlugField(choices=TAG_CHOICES)
    # Get access to all models in the project
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.tag

    class Meta:
        verbose_name_plural = "tags"
