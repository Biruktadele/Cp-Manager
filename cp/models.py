from django.db import models
# from django.contrib.auth.models import User
from core.models import *
# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    deep_link = models.URLField(max_length=200 , unique=True)  # add unique=True 
    solved = models.BooleanField(default=False)
    solution = models.TextField(blank=True, null=True)
    timetaken = models.DateTimeField(blank=True, null=True)
    programming_language = models.CharField(max_length=100, blank=True, null=True)
    is_daily_problem = models.BooleanField(default=False)
    topic_tags = models.JSONField(default=list)
    rating = models.IntegerField(default=1500)

    def __str__(self):
        return self.title

class Ranklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problems_solved = models.IntegerField(default=0)
    rating = models.IntegerField(default=1500)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
class TeamRanklist(models.Model):
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
    problems_solved = models.IntegerField(default=0)
    rating = models.IntegerField(default=1500)

    def __str__(self):
        return f"{self.team_name} - {self.problems_solved} problems solved"

class Contest(models.Model):
    contest_id = models.IntegerField(unique=True , null=True, blank=True)
    title = models.CharField(max_length=200)
    is_rated = models.BooleanField(default=False)
    contestlink = models.URLField(max_length=200)
    startTimeSeconds = models.IntegerField(default=0)
    durationSeconds = models.IntegerField(default=0)
    phase = models.CharField(max_length=50, default='FINISHED')
    preparedBy = models.CharField(max_length=100, blank=True, null=True)
    contest_type = models.CharField(max_length=50, choices=[('Div. 1', 'Div. 1'), ('Div. 2', 'Div. 2'), ('Community', 'Community')], default='Div. 2')
    
    def __str__(self):
        return self.title
class Standing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    penalty_time = models.IntegerField(default=0)  # in minutes
    problemResults = models.JSONField(default=list)  # Store problem results as a JSON object
    rating_change = models.IntegerField(default=0)
    participant_type = models.CharField(max_length=50, choices=[('Contestant', 'Contestant'), ('OutOfCompetition', 'OutOfCompetition'), ('Virtual', 'Virtual'), ('Practice', 'Practice')], default='Contestant')
    is_rated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.contest.title}"

class TeamStanding(models.Model):
    team_name = models.ForeignKey(Team , on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    penalty_time = models.IntegerField(default=0)  # in minutes
    problemResults = models.JSONField(default=list)  # Store problem results as a JSON object
    rating_change = models.IntegerField(default=0)
    participant_type = models.CharField(max_length=50, choices=[('Contestant', 'Contestant'), ('OutOfCompetition', 'OutOfCompetition'), ('Virtual', 'Virtual'), ('Practice', 'Practice')], default='Contestant')
    is_rated = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.team_name} - {self.contest.title}"

