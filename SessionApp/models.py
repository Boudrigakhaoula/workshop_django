from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
import random, string

def generate_submission_id():
    return "SUB-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def validate_keywords(value):
    keywords_list = [kw.strip() for kw in value.split(",") if kw.strip()]
    if len(keywords_list) > 10:
        raise ValidationError("Maximum 10 mots-clés autorisés.")

class Session(models.Model):
    conference = models.ForeignKey("ConferenceApp.Conference", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[A-Za-z0-9]+$', "Nom de salle invalide")]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sessions"

    def clean(self):
        if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
            raise ValidationError("La session doit être dans la période de la conférence.")
        if self.end_time <= self.start_time:
            raise ValidationError("Heure fin doit être supérieure à heure début.")

    def __str__(self):
        return self.title

class Submission(models.Model):
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE)
    conference = models.ForeignKey("ConferenceApp.Conference", on_delete=models.CASCADE)

    submission_id = models.CharField(max_length=12, primary_key=True, editable=False)

    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.CharField(max_length=500, validators=[validate_keywords])
    paper = models.FileField(upload_to='papers/', validators=[FileExtensionValidator(['pdf'])])

    status = models.CharField(
        max_length=20,
        choices=[('Submitted', 'Submitted'),
                 ('Under Review', 'Under Review'),
                 ('Accepted', 'Accepted'),
                 ('Rejected', 'Rejected')],
        default='Submitted'
    )

    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Submissions"

    def clean(self):
        # Vérifier que la soumission est pour une conférence à venir
        if self.submission_date and self.submission_date >= self.conference.start_date:
            raise ValidationError("Soumission possible uniquement avant le début de la conférence.")

        # Limiter à 3 soumissions par jour par utilisateur
        today_submissions = Submission.objects.filter(
            user=self.user,
            submission_date=self.submission_date
        ).exclude(submission_id=self.submission_id).count()

        if today_submissions >= 3:
            raise ValidationError("Vous avez atteint la limite de 3 soumissions pour aujourd'hui.")

    def save(self, *args, **kwargs):
        if not self.submission_id:
            self.submission_id = generate_submission_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
