from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geoModels

# Create your models here.

class River(models.Model):
    river_name = models.CharField(max_length=50,null=True, blank=True)
    river_description = models.TextField(null=True, blank=True)
    route = geoModels.LineStringField(null=True, blank=True)
    get_in = geoModels.PointField(null=True, blank=True)
    get_out = geoModels.PointField(null=True, blank=True)

class Note(models.Model):
    river = models.ForeignKey(River, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-datetime_created']

class PublicComment(models.Model):
    river = models.ForeignKey(River, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-datetime_created']