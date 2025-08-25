from django.urls import path
from LeaderboardEntry import views
urlpatterns = [
    path('api/leaderboard/', views.LeaderboardEntryList.as_view(), name='leaderboardentry-list'),
]
