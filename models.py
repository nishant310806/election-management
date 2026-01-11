from django.db import models
from django.contrib.auth.models import User


class Election(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name="candidates"
    )
    name = models.CharField(max_length=100)
    manifesto = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.election.title})"


class Vote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} voted in {self.election.title}"

