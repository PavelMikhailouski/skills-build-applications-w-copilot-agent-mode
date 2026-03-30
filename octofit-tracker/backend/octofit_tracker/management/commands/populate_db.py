from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient
from django.conf import settings

# Define test data
USERS = [
    {"name": "Tony Stark", "email": "tony@marvel.com", "team": "Marvel"},
    {"name": "Steve Rogers", "email": "steve@marvel.com", "team": "Marvel"},
    {"name": "Bruce Wayne", "email": "bruce@dc.com", "team": "DC"},
    {"name": "Clark Kent", "email": "clark@dc.com", "team": "DC"},
]
TEAMS = [
    {"name": "Marvel", "members": ["tony@marvel.com", "steve@marvel.com"]},
    {"name": "DC", "members": ["bruce@dc.com", "clark@dc.com"]},
]
ACTIVITIES = [
    {"user_email": "tony@marvel.com", "activity": "Running", "duration": 30},
    {"user_email": "steve@marvel.com", "activity": "Cycling", "duration": 45},
    {"user_email": "bruce@dc.com", "activity": "Swimming", "duration": 25},
    {"user_email": "clark@dc.com", "activity": "Flying", "duration": 60},
]
LEADERBOARD = [
    {"user_email": "clark@dc.com", "score": 100},
    {"user_email": "tony@marvel.com", "score": 90},
    {"user_email": "steve@marvel.com", "score": 80},
    {"user_email": "bruce@dc.com", "score": 70},
]
WORKOUTS = [
    {"name": "Super Strength", "suggested_for": "DC"},
    {"name": "Genius Tech", "suggested_for": "Marvel"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email for users
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
