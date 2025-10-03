from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *


class ProblemViewSet(viewsets.ModelViewSet):
	"""CRUD for CP problems."""
	queryset = Problem.objects.all().order_by('id')
	serializer_class = ProblemSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ...existing code...
class DailyProblemViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for daily problems."""
    # avoid DB access at import time
    queryset = Problem.objects.none()
    serializer_class = DailyProblemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # evaluated per-request, safe during migrations/startup
        return Problem.objects.filter(is_daily_problem=True).order_by('-id')
# ...existing code...

class Div2ContestViewSet(viewsets.ModelViewSet):
    """CRUD for Contests."""
    queryset = Contest.objects.all().filter(contest_type='Div. 2').order_by('-startTimeSeconds')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return div2CreateContestSerializer
        return Div2ContestSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['contest_type'] = 'Div. 2'
        return context

class CommunityContestViewSet(viewsets.ModelViewSet):
    """CRUD for Contests."""
    queryset = Contest.objects.all().filter(contest_type='Community').order_by('-startTimeSeconds')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return div2CreateContestSerializer
        return Div2ContestSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['contest_type'] = 'Community'
        return context 
    
class Div1ContestViewSet(viewsets.ModelViewSet):
    """CRUD for Contests."""
    queryset = Contest.objects.all().filter(contest_type='Div. 1').order_by('-startTimeSeconds')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Div1CreateContestSerializer
        return Div1ContestSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['contest_type'] = 'Div. 1'
        return context

class Div2StandingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        contest_pk = self.kwargs['div2contest_pk']
        return Standing.objects.filter(contest_id=contest_pk).order_by('-problems_solved', 'penalty_time')
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Div2CreateContestStandingsSerializer
        return Div2ContestStandingsSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['div2contest_pk'] = self.kwargs['div2contest_pk']
        context['contest_type'] = 'Div. 2'
        return context
class CommunityStandingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        contest_pk = self.kwargs['communitycontest_pk']
        return Standing.objects.filter(contest_id=contest_pk).order_by('-problems_solved', 'penalty_time')
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Div2CreateContestStandingsSerializer
        return Div2ContestStandingsSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['div2contest_pk'] = self.kwargs['communitycontest_pk']
        context['contest_type'] = 'Community'
        return context

class Div1StandingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        contest_pk = self.kwargs['div1contest_pk']
        print(contest_pk)
        return TeamStanding.objects.filter(contest_id=contest_pk).order_by('-problems_solved', 'penalty_time')
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Div1CreateStandingSerializer
        return Div1ContestStandingsSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['div1contest_pk'] = self.kwargs['div1contest_pk']
        context['contest_type'] = 'Div. 1'
        return context

class Div2RankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().filter(div='Div. 2').order_by('-rating')
    serializer_class = Div2RankSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class CommunityRankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().filter(div='Community').order_by('-rating')
    serializer_class = CommunityRankSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class Div1RankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all().order_by('-team_rating')
    serializer_class = Div1RankSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class healthCheckViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    def list(self, request):
        return Response({"status": "ok"})