from django.db import models
from UserApp.models import User

class Conference(models.Model):

    THEME_CHOICES = [
        ('AI', 'Computer Science & Artificial Intelligence'),
        ('ENG', 'Science & Engineering'),
        ('SOC', 'Social Sciences & Education'),
        ('INT', 'Interdisciplinary Themes')
    ]

    title = models.CharField(max_length=255)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES)
    location = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#####
class OrganizingCommittee(models.Model):

    ROLE_CHOICES = [
        ('chair', 'Chair'),
        ('co-chair', 'Co-Chair'),
        ('member', 'Member')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    committee_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_joined = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.committee_role})"
