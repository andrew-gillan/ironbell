from django.db import models

class Competition(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __unicode__(self):
        return unicode(self.name)

class Athlete(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    BELL_WEIGHT_CHOICES = (
        (6.0, '6kg'),
        (8.0, '8kg'),
        (10.0, '10kg'),
        (12.0, '12kg'),
        (16.0, '16kg'),
        (20.0, '20kg'),
        (24.0, '24kg'),
        (28.0, '28kg'),
        (32.0, '32kg'),
    )
    WEIGHT_DIVISION_CHOICES = (
        #MALE & FEMALE
        ('up to 53kg',  'up to 53kg'),
        ('up to 58kg',  'up to 58kg'),
        ('up to 63kg',  'up to 63kg'),
        ('up to 68kg',  'up to 68kg'),
        #FEMALE ONLY
        ('over 63kg',   'over 63kg'),
        ('over 68kg',   'over 68kg'),
        #MALE ONLY
        ('up to 73kg',  'up to 73kg'),
        ('up to 78kg',  'up to 78kg'),
        ('up to 85kg',  'up to 85kg'),
        ('up to 95kg',  'up to 95kg'),
        ('over 95kg',   'over 95kg'),
        ('up to 105kg', 'up to 105kg'),
        ('over 105kg',  'over 105kg'),
    )
    AGE_CLASS_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('youth', 'Youth'),
        ('junior', 'Junior'),
        ('masters', 'Masters'),
        ('team', 'Team'),
    )
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.FloatField()
    weight_class = models.CharField(max_length=200, choices=WEIGHT_DIVISION_CHOICES)
    age_class = models.CharField(max_length=200, choices=AGE_CLASS_CHOICES)
    apparatus_weight = models.FloatField(choices=BELL_WEIGHT_CHOICES)

    def __unicode__(self):
        return unicode(self.name)

class Judge(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.name)

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('biathlon-jerk', 'Biathlon Jerk'),
        ('biathlon-snatch', 'Biathlon Snatch'),
        ('longcycle', 'Long Cycle'),
        ('snatch', 'Snatch Only'),
        ('combined-snatch', 'Snatch'),
        ('oalc', 'OALC'),
        ('chairpress', 'Chair Press Relay'),
    )
    competition = models.ForeignKey(Competition, default=1)
    name = models.CharField(max_length=200)
    scheduled_start_datetime = models.DateTimeField(verbose_name="Scheduled Start")
    duration_seconds = models.IntegerField(default=600) # 10 minutes
    event_type = models.CharField(max_length=200, choices=EVENT_TYPE_CHOICES)
    timer = models.CharField(max_length=5, default='00:00')
    start_time = models.IntegerField(default=0)
    countdown_duration = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.name)

    def competition_name(self):
        return self.competition.name

    @property
    def sorted_scoringstation_set(self):
        return self.scoringstation_set.order_by('station_num', 'athlete__gender', 'athlete__weight_class', 'athlete__apparatus_weight', 'score')

    @property
    def duration_minutes(self):
        secs = self.duration_seconds
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        return '%02d:%02d' % (mins, secs)

    @property
    def current_event_id(self):
        if self.event_locations.all().count() > 0:
            current_event = self.event_locations.all()[0].current_event
            if current_event:
                return current_event.id
            else:
                return -1
        else:
            return -1

class EventLocation(models.Model):
    name = models.CharField(max_length=200)
    events = models.ManyToManyField(Event, blank=True, related_name='event_locations')
    current_event = models.ForeignKey(Event, blank=True, null=True, related_name='current_event')

    def __unicode__(self):
        return unicode(self.name)

class ScoringStation(models.Model):
    station_num = models.IntegerField()
    athlete = models.ForeignKey(Athlete)
    judge = models.ForeignKey(Judge)
    event = models.ForeignKey(Event)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode('Athlete: {} - Score: {} - Judge: {} - Station: {}'.format(
            self.athlete.name, self.score, self.judge.name, self.station_num))
