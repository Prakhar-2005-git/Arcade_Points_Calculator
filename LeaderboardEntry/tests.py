from django.test import TestCase
from .models import LeaderboardEntry
from rest_framework.test import APIClient
from rest_framework import status

class LeaderboardEntryModelTest(TestCase):
    def setUp(self):
        self.entry = LeaderboardEntry.objects.create(
            user_name="Test User",
            skill_badges_completed=5,
            arcade_games_completed=3,
            trivia_games_completed=2,
            lab_free_courses_completed=1,
            access_code_redemption_status="Active",
            milestone_earned="Milestone 1"
        )

    def test_entry_creation(self):
        self.assertEqual(self.entry.user_name, "Test User")
        self.assertEqual(self.entry.skill_badges_completed, 5)

    def test_string_representation(self):
        self.assertEqual(str(self.entry), "Test User")

class LeaderboardEntryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.entry = LeaderboardEntry.objects.create(
            user_name="Test User",
            skill_badges_completed=5,
            arcade_games_completed=3,
            trivia_games_completed=2,
            lab_free_courses_completed=1,
            access_code_redemption_status="Active",
            milestone_earned="Milestone 1"
        )

    def test_get_leaderboard_entries(self):
        response = self.client.get('/api/leaderboard/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the entry is returned
