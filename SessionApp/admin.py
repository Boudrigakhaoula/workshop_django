from django.contrib import admin
from .models import Session, Submission

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'conference', 'session_day', 'start_time', 'end_time', 'room')
    list_filter = ('conference', 'session_day')
    search_fields = ('title', 'topic', 'room')
    ordering = ['session_day', 'start_time']
    date_hierarchy = 'session_day'
    
    fieldsets = (
        ("Informations de base", {
            'fields': ('conference', 'title', 'topic')
        }),
        ("Planning", {
            'fields': ('session_day', 'start_time', 'end_time', 'room')
        }),
    )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    
    # Affichage dans la liste avec méthode short_abstract personnalisée
    list_display = ('title', 'status', 'user', 'conference', 'submission_date', 'payed', 'short_abstract')
    list_filter = ('status', 'payed', 'conference', 'submission_date')
    search_fields = ('title', 'keywords', 'user__username')
    
    # Edition directe depuis la liste
    list_editable = ('status', 'payed')
    
    # Champs en lecture seule
    readonly_fields = ('submission_id', 'submission_date')
    
    # Organisation des champs par sections
    fieldsets = (
        ("Infos générales", {
            'fields': ('submission_id', 'title', 'abstract', 'keywords')
        }),
        ("Fichier et conférence", {
            'fields': ('paper', 'conference')
        }),
        ("Suivi", {
            'fields': ('status', 'payed', 'submission_date', 'user')
        }),
    )
    
    # Ordering et navigation par date
    ordering = ['-submission_date']
    date_hierarchy = 'submission_date'
    
    # Méthode personnalisée pour tronquer l'abstract
    def short_abstract(self, obj):
        """Tronque l'abstract à 50 caractères pour l'affichage rapide"""
        if len(obj.abstract) > 50:
            return obj.abstract[:50] + "..."
        return obj.abstract
    short_abstract.short_description = "Résumé court"
    
    # Actions personnalisées
    actions = ['mark_as_payed', 'accept_submissions']
    
    def mark_as_payed(self, request, queryset):
        """Marquer plusieurs soumissions comme payées"""
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} soumission(s) marquée(s) comme payée(s).")
    mark_as_payed.short_description = "Marquer comme payé"
    
    def accept_submissions(self, request, queryset):
        """Accepter plusieurs soumissions en un clic"""
        updated = queryset.update(status='Accepted')
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")
    accept_submissions.short_description = "Accepter les soumissions sélectionnées"
