from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random, string

# Générer ID utilisateur : USERXXXX (longueur 8)
def generate_user_id():
    return "USER" + ''.join(random.choices(string.digits, k=4))

# Validateur pour user_id : exactement 8 caractères, format USERXXXX
def validate_user_id_length(value):
    if len(value) != 8:
        raise ValidationError("L'identifiant utilisateur doit avoir exactement 8 caractères.")
    if not value.startswith("USER") or not value[4:].isdigit():
        raise ValidationError("L'identifiant doit respecter le format USERXXXX.")

# Valider email universitaire
def validate_university_email(value):
    allowed_domains = ["esprit.tn", "insat.tn", "fst.tn", "isamm.tn"]
    domain = value.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError("Email doit appartenir à un domaine universitaire (ex: @esprit.tn)")

# Nom / prénom : lettres + espaces
name_validator = RegexValidator(
    regex=r'^[A-Za-z\s-]+$',
    message="Nom et prénom doivent contenir uniquement des lettres."
)

class User(AbstractUser):

    user_id = models.CharField(
        primary_key=True,
        max_length=8,
        editable=False,
        validators=[validate_user_id_length]
    )

    email = models.EmailField(unique=True, validators=[validate_university_email])
    first_name = models.CharField(max_length=50, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])

    role = models.CharField(
        max_length=20,
        choices=[
            ('participant', 'Participant'),
            ('organizer', 'Organizer'),
            ('committee', 'Committee Member')
        ],
        default='participant'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = generate_user_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_id})"
