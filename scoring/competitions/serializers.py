from django.forms import widgets
from rest_framework import serializers
from competitions.models import Event, ScoringStation

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'duration_seconds')

class EventTimerSerializer(serializers.ModelSerializer):
    current_event_id = serializers.SerializerMethodField('get_current_event_id')
    class Meta:
        model = Event
        fields = ('id', 'timer', 'current_event_id')
    def get_current_event_id(self, obj):
        current_event = obj.event_locations.all()[0].current_event
        if current_event:
            return current_event.id
        else:
            return -1

class EventStartTimeSerializer(serializers.ModelSerializer):
    current_event_id = serializers.SerializerMethodField('get_current_event_id')
    station_score = serializers.SerializerMethodField('get_station_score')
    class Meta:
        model = Event
        fields = ('id', 'start_time', 'station_score', 'countdown_duration', 'current_event_id')
    def get_current_event_id(self, obj):
        current_event = obj.event_locations.all()[0].current_event
        if current_event:
            return current_event.id
        else:
            return -1
    def get_station_score(self, obj):
        return {'station1':obj.scoringstation_set.all()[0].score, 'station2':obj.scoringstation_set.all()[1].score, 'station3':obj.scoringstation_set.all()[2].score, 'station4':obj.scoringstation_set.all()[3].score}

class ScoringStationSerializer(serializers.ModelSerializer):
    current_event_id = serializers.SerializerMethodField('get_current_event_id')
    event = serializers.SlugRelatedField(read_only=True, slug_field='timer')
    class Meta:
        model = ScoringStation
        fields = ('id', 'score', 'event', 'current_event_id')
    def get_current_event_id(self, obj):
        current_event = obj.event.event_locations.all()[0].current_event
        if current_event:
            return current_event.id
        else:
            return -1
