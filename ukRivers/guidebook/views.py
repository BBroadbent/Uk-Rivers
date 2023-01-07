from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DeleteView
from guidebook.models import *
from geojson import Feature, Point, FeatureCollection, LineString, dumps, loads
from django.contrib.gis.geos import GEOSGeometry
from geojson_length import calculate_distance, Unit
import json, datetime
import requests
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
        context['rivers'] = rivers.order_by('river_name')
        return context

class RiverView(TemplateView):
    template_name = "river.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        river = River.objects.get(id=kwargs['riverID'])
        context['riverRoute'] = Feature(geometry=LineString(river.route), properties={"riverName": river.river_name, 'riverID': river.id})
        context['riverGetIn'] = Point(river.get_in.location)
        context['riverGetOut'] = Point(river.get_out.location)
        context['riverLength'] = round(calculate_distance(context['riverRoute'], Unit.meters)/1000,1)
        context['river'] = river

        if river.gauge_measure_id:
            # This request gets the levels to draw the graph 
            url = "http://environment.data.gov.uk/flood-monitoring/id/stations/%s/readings?since=%s"%(river.gauge_measure_id, (datetime.datetime.now()-datetime.timedelta(days=3)).strftime('%Y-%m-%d'))
            response = requests.request("GET", url)
            context['riverLevels'] = response.json()['items']

            # This request gets the details like river name, max min levels etc.
            url = "http://environment.data.gov.uk/flood-monitoring/id/stations/%s"%(river.gauge_measure_id,)
            response = requests.request("GET", url)
            context['riverLevelDetails'] = response.json()['items']

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
        if(request.POST.get('riverGauge',False)):
            url = "http://environment.data.gov.uk/flood-monitoring/id/stations?RLOIid=%s"%request.POST['riverGauge']
            riverGauge = requests.request("GET", url).json()
            riverGauge = riverGauge['items'][0]['notation']
        else:
            riverGauge = None
        riverRoute = GEOSGeometry(json.dumps(json.loads(request.POST['riverRoute'])['geometry']))
        riverGetIn = GEOSGeometry(json.dumps(json.loads(request.POST['riverGetIn'])['geometry']))
        riverGetOut = GEOSGeometry(json.dumps(json.loads(request.POST['riverGetOut'])['geometry']))

        river = River.objects.create(river_name=request.POST['riverName'], river_description=request.POST['riverDesc'], route=riverRoute, grade=request.POST['riverGrade'], gauge_measure_id=riverGauge)
 
        get_in = Place.objects.create(river=river, location=riverGetIn, description="Main get in", place_type="put", created_by_user=request.user)
        get_out = Place.objects.create(river=river, location=riverGetOut, description="Main get out", place_type="take", created_by_user=request.user)

        river.get_in = get_in
        river.get_out = get_out
        river.save()

        return redirect('/river/%s'%river.id)

class NoteDeleteView(DeleteView):
    model = Note
    success_url = '/river/{river_id}'

class CommentDeleteView(DeleteView):
    model = PublicComment
    success_url = '/river/{river_id}'