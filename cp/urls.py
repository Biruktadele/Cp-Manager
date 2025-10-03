from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'problems', ProblemViewSet, basename='problem')
router.register(r'daily', DailyProblemViewSet, basename='dailyproblem')
router.register(r'div2contests', Div2ContestViewSet, basename='div2contest')
router.register(r'communitycontests', CommunityContestViewSet, basename='communitycontest')
router.register(r'div1contests', Div1ContestViewSet, basename='div1contest')
router.register(r'div2rankings', Div2RankingViewSet, basename='div2ranking')
router.register(r'communityrankings', CommunityRankingViewSet, basename='communityranking')
router.register(r'div1rankings', Div1RankingViewSet, basename='div1ranking')
router.register(r'health', healthCheckViewSet, basename='healthcheck')

nested_router = routers.NestedDefaultRouter(router, r'div2contests', lookup='div2contest')
nested_community_router = routers.NestedDefaultRouter(router, r'communitycontests', lookup='communitycontest')
nested_div1_router = routers.NestedDefaultRouter(router, r'div1contests', lookup='div1contest')


nested_div1_router.register(r'standings', Div1StandingViewSet, basename='div1conteststandings')
nested_router.register(r'standings', Div2StandingViewSet, basename='div2conteststandings')
nested_community_router.register(r'standings', CommunityStandingViewSet, basename='communityconteststandings')


# router.register(r'deai', SubmitSolutionViewSet, basename='submitsolution')
urlpatterns = router.urls + nested_router.urls + nested_community_router.urls + nested_div1_router.urls
