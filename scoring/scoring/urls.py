from django.conf.urls import patterns, include, url

from django.contrib import admin
import scoring

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'scoring.views.index', name='index'),
    url(r'^scoring/(?P<competition_id>\d+)/$', 'scoring.views.competition_detail', name='competition_detail'),
    url(r'^scoring/(\d+)/event/(?P<event_id>\d+)/$', 'scoring.views.event_detail', name='event_detail'),
    url(r'^scoring/(\d+)/event/(?P<event_id>\d+)/timer/$', 'scoring.views.timer', name='timer'),
    url(r'^scoring/(\d+)/event/(?P<event_id>\d+)/station/(?P<station_num>\d+)/$', 'scoring.views.station', name='station'),
    url(r'^scoring/(\d+)/event/(?P<event_id>\d+)/station_score/(?P<station_num>\d+)/$', 'scoring.views.station_score', name='station_score'),
    url(r'^scoring/(\d+)/event/(?P<event_id>\d+)/judging/(?P<station_num>\d+)/$', 'scoring.views.judging', name='judging'),
    url(r'^api/event/(?P<pk>[0-9]+)$', 'scoring.views.json_event'),
    url(r'^api/score/(?P<event_id>\d+)/(?P<station_num>\d+)$', 'scoring.views.json_score'),
    url(r'^api/timer/(?P<pk>[0-9]+)$', 'scoring.views.json_timer'),
)
