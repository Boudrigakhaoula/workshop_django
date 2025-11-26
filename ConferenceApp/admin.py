from django.contrib import admin
from .models import Conference, OrganizingCommittee
from SessionApp.models import Submission

# Personnalisation des en-têtes de l'interface admin
admin.site.site_header = "Gestion des Conférences Scientifiques"
admin.site.site_title = "Admin Conférence"
admin.site.index_title = "Tableau de bord - Administration des Conférences"

# Inline StackedInline pour les soumissions
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 0
    readonly_fields = ('submission_id', 'submission_date')
    fields = ('submission_id', 'title', 'abstract', 'keywords', 'paper', 'status', 'payed', 'submission_date', 'user')
    
# Inline TabularInline pour les soumissions (version alternative)
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 0
    readonly_fields = ('submission_id', 'submission_date')
    fields = ('title', 'status', 'user', 'payed')

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    
    # Affichage dans la liste avec méthode duration personnalisée
    list_display = ('title', 'theme', 'location', 'start_date', 'end_date', 'duration')
    list_filter = ('theme', 'location', 'start_date')
    search_fields = ('title', 'description', 'location')
    
    # Organisation des champs en sections
    fieldsets = (
        ("Informations générales", {
            'fields': ('title', 'theme', 'description')
        }),
        ("Logistique", {
            'fields': ('location', 'place', 'start_date', 'end_date')
        }),
    )
    
    # Ordering et navigation par calendrier
    ordering = ['start_date']
    date_hierarchy = 'start_date'
    
    # Inline pour afficher les soumissions (vous pouvez alterner entre Stacked et Tabular)
    inlines = [SubmissionStackedInline]  # Changez en SubmissionTabularInline pour tester la version tabulaire
    
    # Méthode personnalisée pour calculer la durée
    def duration(self, obj):
        """Calcule la durée en jours entre start_date et end_date"""
        if obj.start_date and obj.end_date:
            delta = obj.end_date - obj.start_date
            return f"{delta.days} jour(s)"
        return "N/A"
    duration.short_description = "Durée"

@admin.register(OrganizingCommittee)
class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'committee_role', 'date_joined')
    list_filter = ('committee_role', 'conference')
    search_fields = ('user__username', 'user__email', 'conference__title')
