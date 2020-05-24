from django.contrib import admin

from django.http import HttpResponse
from django.urls import path
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required

#Import nécessaire à la vue pour l'envoi de mails
from .forms import CourrielForm
# from site_sad.settings import EXPEDITEUR
from site_sad.settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail

from .models import CustomUser, Actualite, Cours


# Partie pour personaliser l'interface
admin.site.site_header = "Gestion de la S.A.D"

class CoursAdmin(admin.ModelAdmin):
    search_fields = ['date', 'adresse', 'texte_etudie']
    list_display = ['date', 'heure', 'adresse']
    list_filter = ['date', 'adresse']
    
class ActualiteAdmin(admin.ModelAdmin):
    search_fields = ['nom', 'texte', 'date']
    list_display = ['nom', 'texte', 'date']
    list_filter = ['nom', 'date']
    
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_display = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['username', 'last_name', 'email']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Actualite, ActualiteAdmin)
admin.site.register(Cours, CoursAdmin)

    

# Partie pour afficher dans la liste d'administration une url
class Courriels(models.Model):

    class Meta:
        verbose_name_plural = 'Courriels'
        app_label = 'gestion'

@staff_member_required       
def my_custom_view(request):
    if request.method == 'POST':
        form = CourrielForm(request.POST)
        if form.is_valid():
            titre = form.cleaned_data.get('Titre')
            texte = form.cleaned_data.get('Texte')
            destinataire = form.cleaned_data.get('Destinataires')

            # Partie pour composer la liste de diffusion en évitant les doublons d'adresse
            liste_diffusion = []
            if len(destinataire) == 1:
                if 'membres' in destinataire:
                    nb_membres = CustomUser.objects.filter(membre='o')
                    for elt in nb_membres:
                        liste_diffusion.append(elt.email)
                else:
                    nb_membres = CustomUser.objects.filter(newsletter='o')
                    for elt in nb_membres:
                        liste_diffusion.append(elt.email)
                        
            elif len(destinataire) == 2:
                nb_membres = CustomUser.objects.filter(membre='o')
                for elt in nb_membres:
                    liste_diffusion.append(elt.email)
                nb_listes = CustomUser.objects.filter(newsletter='o')
                for elt in nb_listes:
                    if elt.email not in liste_diffusion:
                        liste_diffusion.append(elt.email)
                        
            # Partie pour l'envoi des mails
            send_mail(
                # 'Subject here',
                titre,
                # 'Here is the message.',
                texte,
                # 'your.application@gmail.com',
                # EXPEDITEUR,
                EMAIL_HOST_USER,
                # ['to@mail.com']
                liste_diffusion
            )

            return redirect(reverse('admin:index'))
        
    form = CourrielForm()
    return render(request, 'courriel.html', {'form': form})

class CourrielsAdmin(admin.ModelAdmin):
    model = Courriels
    
    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path/', my_custom_view, name=view_name),
        ]
admin.site.register(Courriels, CourrielsAdmin)