from rest_framework import serializers
from .models import LeaderboardEntry

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    achieved_milestone = serializers.CharField(source='milestone_earned', read_only=True)
    total_points = serializers.IntegerField(read_only=True)

    class Meta:
        model = LeaderboardEntry
        fields = [
            'user_name',
            'access_code_redemption_status',
            'skill_badges_completed',
            'arcade_games_completed',
            'trivia_games_completed',
            'lab_free_courses_completed',
            'achieved_milestone',
            'names_of_completed_skill_badges',
            'names_of_completed_arcade_games',
            'names_of_completed_trivia_games',
            'names_of_completed_lab_free_courses',
            'profile_url_status',
            'google_cloud_skills_boost_profile_url',
            'closest_milestone',
            'missing_for_closest_milestone',
            'total_points'  
        ]
