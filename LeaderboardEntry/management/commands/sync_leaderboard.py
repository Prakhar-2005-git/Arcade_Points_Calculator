from django.core.management.base import BaseCommand
import requests
import json
import csv
import os
from django.conf import settings
from LeaderboardEntry.models import LeaderboardEntry

class Command(BaseCommand):
    help = 'Syncs leaderboard data from local CSV file to the database.'

    def handle(self, *args, **kwargs):
        # Get the path to the CSV file
        csv_path = os.path.join(settings.BASE_DIR, 'LeaderboardEntry', 'uploads', 'leaderboard_data.csv')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING('No CSV file found. Please upload a CSV file first.'))
            return
        
        # Read data from CSV file
        data = []
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        count = 0
        milestones = [
            {
                'name': 'Milestone 1',
                'arcade_games': 6,
                'trivia_games': 5,
                'skill_badges': 14,
                'lab_free_courses': 6,
            },
            {
                'name': 'Milestone 2',
                'arcade_games': 8,
                'trivia_games': 6,
                'skill_badges': 28,
                'lab_free_courses': 12,
            },
            {
                'name': 'Milestone 3',
                'arcade_games': 10,
                'trivia_games': 7,
                'skill_badges': 38,
                'lab_free_courses': 18,
            },
            {
                'name': 'Ultimate Milestone',
                'arcade_games': 12,
                'trivia_games': 8,
                'skill_badges': 52,
                'lab_free_courses': 24,
            },
        ]
        for user in data:
            if any(k in user for k in ['User Name', '# of Skill Badges Completed', '# of Arcade Games Completed', '# of Trivia Games Completed', '# of Lab-free Courses Completed']):
                skill_badges = int(user.get('# of Skill Badges Completed', 0) or 0)
                arcade_games = int(user.get('# of Arcade Games Completed', 0) or 0)
                trivia_games = int(user.get('# of Trivia Games Completed', 0) or 0)
                lab_free_courses = int(user.get('# of Lab-free Courses Completed', 0) or 0)
                skill_badge_points = skill_badges // 2
                arcade_game_points = arcade_games
                if arcade_games >= 5:
                    arcade_game_points = 6
                trivia_points = trivia_games
                total_points = skill_badge_points + arcade_game_points + trivia_points

                achieved_milestone = None
                closest_milestone = None
                achieved_index = None
                missing_for_closest_milestone = None
                for idx, milestone in enumerate(reversed(milestones)):
                    if (arcade_games >= milestone['arcade_games'] and
                        trivia_games >= milestone['trivia_games'] and
                        skill_badges >= milestone['skill_badges'] and
                        lab_free_courses >= milestone['lab_free_courses']):
                        achieved_milestone = milestone['name']
                        achieved_index = len(milestones) - 1 - idx
                        break
                if achieved_index is not None:
                    if achieved_index + 1 < len(milestones):
                        next_milestone = milestones[achieved_index + 1]
                        closest_milestone = next_milestone['name']
                        missing_for_closest_milestone = {
                            'arcade_games': max(0, next_milestone['arcade_games'] - arcade_games),
                            'trivia_games': max(0, next_milestone['trivia_games'] - trivia_games),
                            'skill_badges': max(0, next_milestone['skill_badges'] - skill_badges),
                            'lab_free_courses': max(0, next_milestone['lab_free_courses'] - lab_free_courses),
                        }
                    else:
                        closest_milestone = None
                        missing_for_closest_milestone = None
                else:
                    for milestone in milestones:
                        missing = {
                            'arcade_games': max(0, milestone['arcade_games'] - arcade_games),
                            'trivia_games': max(0, milestone['trivia_games'] - trivia_games),
                            'skill_badges': max(0, milestone['skill_badges'] - skill_badges),
                            'lab_free_courses': max(0, milestone['lab_free_courses'] - lab_free_courses),
                        }
                        if any(v > 0 for v in missing.values()):
                            closest_milestone = milestone['name']
                            missing_for_closest_milestone = missing
                            break
                entry, created = LeaderboardEntry.objects.update_or_create(
                    user_name=user.get('User Name', ''),
                    defaults={
                        'skill_badges_completed': skill_badges,
                        'arcade_games_completed': arcade_games,
                        'trivia_games_completed': trivia_games,
                        'lab_free_courses_completed': lab_free_courses,
                        'access_code_redemption_status': user.get('Access Code Redemption Status', ''),
                        'milestone_earned': user.get('Milestone Earned', ''),
                        'names_of_completed_skill_badges': user.get('Names of Completed Skill Badges', ''),
                        'names_of_completed_arcade_games': user.get('Names of Completed Arcade Games', ''),
                        'names_of_completed_trivia_games': user.get('Names of Completed Trivia Games', ''),
                        'names_of_completed_lab_free_courses': user.get('Names of Completed Lab-free Courses', ''),
                        'profile_url_status': user.get('Profile URL Status', ''),
                        'google_cloud_skills_boost_profile_url': user.get('Google Cloud Skills Boost Profile URL', ''),
                        'closest_milestone': closest_milestone,
                        'missing_for_closest_milestone': missing_for_closest_milestone,
                        'total_points': total_points,
                    }
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully synced {count} leaderboard entries from CSV file.'))
