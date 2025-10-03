import time
from rest_framework import serializers

from core.serializers import *
from .models import *
from core.models import *
import requests
import hashlib
import time
from . import claculat_rating  , mashup_scraper , get_standing    # Import the rating calculation module

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class SubmitSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.solution = validated_data.get('solution', instance.solution)
        instance.timetaken = validated_data.get('timetaken', instance.timetaken)
        instance.programming_language = validated_data.get('programming_language', instance.programming_language)
        instance.save()
        return instance

class DailyProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        read_only_fields = ['is_daily_problem']

    def create(self, validated_data):
        validated_data['is_daily_problem'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # prevent changing the flag via payload
        validated_data.pop('is_daily_problem', None)
        instance = super().update(instance, validated_data)
        if not instance.is_daily_problem:
            instance.is_daily_problem = True
            instance.save(update_fields=['is_daily_problem'])
        return instance
# ...existing code...

class Div2ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class div2CreateContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['contest_id', 'title', 'is_rated', 'contestlink', 'startTimeSeconds', 'durationSeconds', 'phase', 'preparedBy' , 'contest_type' ]
        read_only_fields = ['title', 'contestlink', 'startTimeSeconds', 'durationSeconds', 'phase', 'preparedBy' , 'contest_type']
    def create(self, validated_data):
        contest_id = validated_data.get('contest_id')
        contest_type = self.context['contest_type']

        contest_data = mashup_scraper.getcontes(contest_id)
        if contest_data:
            validated_data['title'] = contest_data.get('name', '')
            validated_data['contestlink'] = f"https://codeforces.com/gym/{contest_id}"
            validated_data['startTimeSeconds'] = contest_data.get('startTimeSeconds', 0)
            validated_data['durationSeconds'] = contest_data.get('durationSeconds', 0)
            validated_data['phase'] = contest_data.get('phase', 'FINISHED')
            validated_data['preparedBy'] = contest_data.get('preparedBy', '')
            validated_data['contest_type'] = contest_type

        else:
            raise serializers.ValidationError("Could not fetch contest data from Codeforces API.")
        return super().create(validated_data)

class Div1ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'
class Div1CreateContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['contest_id', 'title', 'is_rated', 'contestlink', 'startTimeSeconds', 'durationSeconds', 'phase', 'preparedBy']
        read_only_fields = ['title', 'contestlink', 'startTimeSeconds', 'durationSeconds', 'phase', 'preparedBy']
    def create(self, validated_data):
        contest_id = validated_data.get('contest_id')
        contest_type = self.context['contest_type']
        contest_data = mashup_scraper.getcontes(contest_id)
        if contest_data:
            validated_data['title'] = contest_data.get('name', '')
            validated_data['contestlink'] = f"https://codeforces.com/gym/{contest_id}"
            validated_data['startTimeSeconds'] = contest_data.get('startTimeSeconds', 0)
            validated_data['durationSeconds'] = contest_data.get('durationSeconds', 0)
            validated_data['phase'] = contest_data.get('phase', 'FINISHED')
            validated_data['preparedBy'] = contest_data.get('preparedBy', '')
            validated_data['contest_type'] = contest_type
        else:
            raise serializers.ValidationError("Could not fetch contest data from Codeforces API.")
        return super().create(validated_data)

class Div2ContestStandingsSerializer(serializers.ModelSerializer):
    User = UserSerializer(read_only=True , source = 'user')
    class Meta:
        model = Standing
        fields = ['rank', 'User', 'contest', 'problems_solved', 'penalty_time', 'problemResults', 'rating_change', 'participant_type']
        ordering = ['rank']
class Div2CreateContestStandingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Standing
        fields = ['rank', 'user', 'contest', 'problems_solved', 'penalty_time', 'problemResults', 'rating_change', 'participant_type']
        read_only_fields = ['user', 'contest', 'problems_solved', 'penalty_time', 'problemResults', 'rating_change', 'participant_type', 'rank']
        ordering = ['rank']


    def create(self, validated_data):
        contest_pk = self.context['div2contest_pk']
        contest_instance = Contest.objects.get(pk=contest_pk)
        contest_id = contest_instance.contest_id
        standings = get_standing.fetch_contest_standings(contest_id , contest_pk)

        existing_handles = set(
        Standing.objects.filter(contest_id=contest_instance.id)
                        .values_list("user__username", flat=True)
    )

        new_standings = [s for s in standings if s.user.username not in existing_handles]
        
        for s in new_standings:
            s.is_rated = True
        Standing.objects.bulk_create(new_standings)
        return validated_data

class Div1ContestStandingsSerializer(serializers.ModelSerializer):
    Team = TeamSerializer(read_only=True , source = 'team_name')
    class Meta:
        model = TeamStanding
        fields = ['rank', 'Team', 'contest', 'problems_solved', 'penalty_time', 'problemResults', 'rating_change', 'participant_type']
        ordering = ['rank']
class Div1CreateStandingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamStanding
        fields = ['rank', 'team_name', 'contest', 'problems_solved', 'penalty_time', 'problemResults', 'rating_change', 'participant_type']
        read_only_fields = ['team_name', 'contest', 'problems_solved', 'penalty_time', 'problemResults', 'rating_change', 'participant_type', 'rank']
        ordering = ['rank']


    def create(self, validated_data):
        contest_pk = self.context['div1contest_pk']
        contest_instance = Contest.objects.get(pk=contest_pk)
        contest_id = contest_instance.contest_id
        standings = get_standing.Div1_fetch_contest_standings(contest_id , contest_pk)

        existing_handles = set(
        TeamStanding.objects.filter(contest_id=contest_instance.id)
                        .values_list("team_name__team_name", flat=True)
    )
        print(existing_handles)
        print(standings)
        new_standings = [s for s in standings if s.team_name.team_name not in existing_handles]

        for s in new_standings:
            s.is_rated = True
        TeamStanding.objects.bulk_create(new_standings)
        return validated_data



class Div2RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'rating', 'div', 'codeforces_handle', 'leetcode_handle', 'phone_number', 'avatar', 'bio']
        # read_only_fields = ['user', 'problems_solved', 'rating']
class Div1RankSerializer(serializers.ModelSerializer):
    Members = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ['id', 'team_name', 'team_rating', 'Members']

    def get_Members(self, obj):
        return UserSerializer(obj.members.all(), many=True).data
        # read_only_fields = ['user', 'problems_solved', 'rating']
class CommunityRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'rating', 'div', 'codeforces_handle', 'leetcode_handle', 'phone_number', 'avatar', 'bio']
        # read_only_fields = ['user', 'problems_solved', 'rating']







