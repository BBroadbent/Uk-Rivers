from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DeleteView
from guidebook.models import *
from geojson import Feature, Point, FeatureCollection, LineString, dumps, loads
from django.contrib.gis.geos import GEOSGeometry
import json
# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rivers = River.objects.all()
        riverRoutes = []
        for river in rivers:
            riverRoute = LineString(river.route)
            riverRouteFeature = Feature(geometry=riverRoute, properties={"riverName": river.river_name, 'riverID': river.id})
            riverRoutes.append(riverRouteFeature)

        context['riverFeatureCollection'] = dumps(FeatureCollection(riverRoutes))
        return context

class RiverView(TemplateView):
    template_name = "river.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        river = River.objects.get(id=kwargs['riverID'])
        context['riverRoute'] = Feature(geometry=LineString(river.route), properties={"riverName": river.river_name, 'riverID': river.id})
        context['riverGetIn'] = Point(river.get_in)
        context['riverGetOut'] = Point(river.get_out)
        context['river'] = river

        if self.request.user.is_authenticated:
            context['notes'] = self.request.user.note_set.filter(river=river)
        context['publicComments'] = PublicComment.objects.filter(river=river)

        return context
    def post(self, request, *args, **kwargs):
        if request.GET['action'] == 'newNote':
            note = Note.objects.create(user=request.user, river_id=kwargs['riverID'], note=request.POST['note'])
        if request.GET['action'] == 'newComment':
            comment = PublicComment.objects.create(user=request.user, river_id=kwargs['riverID'], comment=request.POST['comment'])
        
        return redirect(request.path)

class NewRiverView(TemplateView):
    template_name = "newRiver.html"

    def post(self, request, *args, **kwargs):
        riverRoute = GEOSGeometry(json.dumps(json.loads(request.POST['riverRoute'])['geometry']))
        riverGetIn = GEOSGeometry(json.dumps(json.loads(request.POST['riverGetIn'])['geometry']))
        riverGetOut = GEOSGeometry(json.dumps(json.loads(request.POST['riverGetOut'])['geometry']))
        river = River.objects.create(river_name=request.POST['riverName'], river_description=request.POST['riverDesc'], route=riverRoute, get_in=riverGetIn, get_out=riverGetOut)
        return redirect('/river/%s'%river.id)

class NoteDeleteView(DeleteView):
    model = Note
    success_url = '/river/{river_id}'

class CommentDeleteView(DeleteView):
    model = PublicComment
    success_url = '/river/{river_id}'