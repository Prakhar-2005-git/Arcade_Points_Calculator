
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LeaderboardEntry
from .serializers import LeaderboardEntrySerializer
from django.shortcuts import render, redirect

class LeaderboardEntryList(APIView):
	def get(self, request):
		entries = LeaderboardEntry.objects.all()
		serializer = LeaderboardEntrySerializer(entries, many=True)
		
		# Add total_points to the serialized data
		for i, entry_data in enumerate(serializer.data):
			entry_data['total_points'] = (
				(entries[i].skill_badges_completed // 2) + 
				(entries[i].arcade_games_completed if entries[i].arcade_games_completed < 14 else 16) + 
				entries[i].trivia_games_completed
			)
		return Response(serializer.data)
