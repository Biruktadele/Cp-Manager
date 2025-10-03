from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'codeforces_handle', 'leetcode_handle', 'phone_number', 'avatar', 'bio', 'birthday' , 'date_joined' , 'is_staff'] 
        read_only_fields = ['date_joined', 'is_staff']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','phone_number','birthday' ,'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            birthday=validated_data.get('birthday', None)
        )
        return user

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    class Meta:
        model = Team # Access the through model for the ManyToMany relationship
        fields = ['id', 'team_name', 'members', 'team_rating']
        # read_only_fields = ['team_name', 'team_rating']
class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_name', 'members', 'team_rating']
        read_only_fields = ['team_rating']
    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        team, created = Team.objects.get_or_create(**validated_data)
        for member_data in members_data:
            user, created = User.objects.get_or_create(**member_data)
            team.members.add(user)
        return team