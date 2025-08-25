from django.db import models

class LeaderboardEntry(models.Model):
	user_name = models.CharField(max_length=100)
	skill_badges_completed = models.IntegerField(default=0)
	arcade_games_completed = models.IntegerField(default=0)
	trivia_games_completed = models.IntegerField(default=0)
	lab_free_courses_completed = models.IntegerField(default=0)
	access_code_redemption_status = models.CharField(max_length=50, blank=True)
	milestone_earned = models.CharField(max_length=50, blank=True, null=True)
	names_of_completed_skill_badges = models.TextField(blank=True, null=True)
	names_of_completed_arcade_games = models.TextField(blank=True, null=True)
	names_of_completed_trivia_games = models.TextField(blank=True, null=True)
	names_of_completed_lab_free_courses = models.TextField(blank=True, null=True)
	profile_url_status = models.CharField(max_length=100, blank=True)
	google_cloud_skills_boost_profile_url = models.URLField(blank=True)
	closest_milestone = models.CharField(max_length=50, blank=True, null=True)
	missing_for_closest_milestone = models.JSONField(blank=True, null=True)
	total_points = models.IntegerField(default=0)

	def __str__(self):
		return self.user_name
