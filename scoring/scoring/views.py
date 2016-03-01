from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from competitions.serializers import EventSerializer, ScoringStationSerializer, EventTimerSerializer
from competitions.models import Competition, Event, ScoringStation

def index(request):
    competition_list = Competition.objects.order_by('-start_date')[:5]
    context = {'competition_list': competition_list}
    return render(request, 'scoring/index.html', context)

def competition_detail(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'scoring/competition_detail.html', {'competition': competition})

#def events(request, competition_id):
#    return HttpResponse("You're looking at the events of competition %s." % competition_id)

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'scoring/event_detail.html', {'event': event})

def timer(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'scoring/event_timer.html', {'event': event})

def station(request, event_id, station_num):
    event = get_object_or_404(Event, pk=event_id)
    try:
        scoring_station = event.scoringstation_set.get(station_num=station_num)
#        return render(request, 'scoring/station_detail.html', {'scoring_station': scoring_station})
        return render(request, 'scoring/station_card.html', {'scoring_station': scoring_station})
    except ObjectDoesNotExist:
        return render(request, 'scoring/not_in_use.html', {'event_name': event.name, "current_event_id": event.current_event_id, 'station_num': station_num, 'target': 'station'})

def station_score(request, event_id, station_num):
    event = get_object_or_404(Event, pk=event_id)
    scoring_station = event.scoringstation_set.get(station_num=station_num)
    #scoring_station = get_object_or_404(ScoringStation, pk=scoring_station_id)
    return render(request, 'scoring/station_score.html', {'scoring_station': scoring_station})

def judging(request, event_id, station_num):
    event = get_object_or_404(Event, pk=event_id)
    scoring_station = event.scoringstation_set.get(station_num=station_num)
    #scoring_station = get_object_or_404(ScoringStation, pk=scoring_station_id)
    context = {'scoring_station': scoring_station}
    context.update(csrf(request))
    return render(request, 'scoring/judging.html', context)

@api_view(['GET'])
def json_event(request, pk):
    if request.method == 'GET':
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def json_timer(request, pk, format=None):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventTimerSerializer(event)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventTimerSerializer(event, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def json_score(request, event_id, station_num, format=None):
    try:
        event = get_object_or_404(Event, pk=event_id)
        scoring_station = event.scoringstation_set.get(station_num=station_num)
        #scoring_station = ScoringStation.objects.get(pk=pk)
    except ScoringStation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ScoringStationSerializer(scoring_station)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScoringStationSerializer(scoring_station, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
