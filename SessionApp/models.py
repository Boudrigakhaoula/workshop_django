from django.db import models
from ConferenceApp.models import Conference
from UserApp.models import User

class Session(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.conference.title}"
########
class Submission(models.Model):

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.CharField(max_length=500)
    paper = models.FileField(upload_to='papers/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_valid_participant(self):
        return self.status == "Accepted" and self.payed == True

    def __str__(self):
        return f"{self.title} - {self.status}"
