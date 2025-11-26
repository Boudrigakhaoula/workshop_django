from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

title_validator = RegexValidator(
    regex=r'^[A-Za-z\s]+$',
    message="Le titre de la conférence doit contenir uniquement des lettres."
)

class Conference(models.Model):

    THEME_CHOICES = [
        ('AI', 'Computer Science & AI'),
        ('ENG', 'Science & Engineering'),
        ('SOC', 'Social Sciences & Education'),
        ('INT', 'Interdisciplinary Themes'),
    ]

    title = models.CharField(max_length=255, validators=[title_validator])
    theme = models.CharField(max_length=10, choices=THEME_CHOICES)
    location = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(validators=[MinLengthValidator(30)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Conferences"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("La date début doit être avant la date fin.")

    def __str__(self):
        return self.title

class OrganizingCommittee(models.Model):

    ROLE_CHOICES = [
        ('chair', 'Chair'),
        ('co-chair', 'Co-chair'),
        ('member', 'Member'),
    ]

    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    committee_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_joined = models.DateField()

    class Meta:
        verbose_name_plural = "Organizing Committees"

    def __str__(self):
        return f"{self.user.username} - {self.committee_role}"
