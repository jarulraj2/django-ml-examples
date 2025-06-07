from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional user
    game_name = models.CharField(max_length=100, default='unknown')  # Default game name
    started_at = models.DateTimeField(auto_now_add=True)
    stopped_at = models.DateTimeField(null=True, blank=True)

    duration_seconds = models.PositiveIntegerField(default=0)

    clicks = models.PositiveIntegerField(default=0)
    errors = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        username = self.user.username if self.user else "Guest"
        return f"{username} - {self.game_name} @ {self.started_at}"
