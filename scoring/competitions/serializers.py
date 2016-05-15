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
    class Meta:
        model = Event
        fields = ('id', 'start_time', 'countdown_duration', 'current_event_id')
    def get_current_event_id(self, obj):
        current_event = obj.event_locations.all()[0].current_event
        if current_event:
            return current_event.id
        else:
            return -1

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
