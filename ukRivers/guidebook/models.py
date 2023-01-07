from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geoModels

# Create your models here.

class River(models.Model):
    river_name = models.CharField(max_length=50,null=True, blank=True)
    grade = models.CharField(max_length=50,null=True, blank=True)
    river_description = models.TextField(null=True, blank=True)
    route = geoModels.LineStringField(null=True, blank=True)
    get_in = models.ForeignKey('guidebook.Place', on_delete=models.SET_NULL, null=True, blank=True, related_name='get_ins')
    get_out = models.ForeignKey('guidebook.Place', on_delete=models.SET_NULL, null=True, blank=True, related_name='get_outs')
    gauge_measure_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.river_name

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

PLACE_TYPE_CHOICES = [
    ('park', 'Parking'),
    ('put', 'Put In'),
    ('take', 'Take Out'),
]

class Place(models.Model):
    river = models.ForeignKey(River, on_delete=models.CASCADE)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = geoModels.PointField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    place_type = models.TextField(null=True, blank=True, choices=PLACE_TYPE_CHOICES)