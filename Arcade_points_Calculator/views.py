from django.http import JsonResponse
from django.shortcuts import redirect
from LeaderboardEntry.models import LeaderboardEntry
from LeaderboardEntry.serializers import LeaderboardEntrySerializer

def arcade_points_api(request):
    entries = LeaderboardEntry.objects.all()
    
    # Calculate total_points for each entry
    for entry in entries:
        entry.total_points = (
            (entry.skill_badges_completed // 2) + 
            (entry.arcade_games_completed if entry.arcade_games_completed <= 14 else 16) + 
            entry.trivia_games_completed
        )
    
    serializer = LeaderboardEntrySerializer(entries, many=True)
    
    return JsonResponse({'users_summary': serializer.data})
