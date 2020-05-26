from django.contrib import admin

from django.http import HttpResponse
from django.urls import path
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required

#Import nécessaire à la vue pour l'envoi de mails
from .forms import CourrielForm
from site_sad.settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail

#Imports nécessaires au rapport PDF
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.utils import timezone, dateformat
from datetime import timedelta

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

#Partie pour générer un rapport
class Rapports(models.Model):

    class Meta:
        verbose_name_plural = 'Rapports'
        app_label = 'gestion'

@staff_member_required       
def my_custom_view2(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(30, 800, "RAPPORT DE GESTION DE LA S.A.D AU " + dateformat.format(timezone.now(), 'd/m/Y'))
    p.line(20,780,580,780)
    
    p.drawString(60, 740, "Cours")
    p.line(40,730,140,730)
    p.drawString(40, 715, "Nombre de cours programmés à venir le prochain mois : " + str(Cours.objects.filter(date__gte=timezone.now() + timedelta(weeks=4)).count()))
    p.drawString(40, 700, "Nombre de cours programmés à venir la prochaine année : " + str(Cours.objects.filter(date__gte=timezone.now() + timedelta(weeks=52)).count()))
    p.drawString(40, 685, "Nombre de cours effectués lors de la dernière année : " + str(Cours.objects.filter(date__lt=timezone.now() + timedelta(weeks=52)).count()))
    p.drawString(40, 670, "Nombre de cours effectués toutes périodes confondues : " + str(Cours.objects.filter(date__lt=timezone.now()).count()))
    
    p.drawString(60, 610, "Membres")
    p.line (40, 600, 140, 600)
    p.drawString(40, 585, "Nombre de membres toutes périodes confondues : " + str(CustomUser.objects.filter(membre="o").count()))
    p.drawString(40, 570, "Nombre de membres actuels : " + str(CustomUser.objects.filter(is_active=True, membre="o").count()))
    p.drawString(40, 555, "Nombre de membres actuels inscrits à la newsletter : " + str(CustomUser.objects.filter(membre="o", newsletter="o").count()))
    p.drawString(40, 540, "Nombre d'inscrits uniquement à la newsletter : " + str(CustomUser.objects.filter(newsletter="n").count()))
    
    p.drawString(60, 480, "Actualités")
    p.line(40, 470, 140, 470)
    p.drawString(40, 455, "Nombre d'actualités publiées lors du dernier mois : " + str(Actualite.objects.filter(date__lte=timezone.now() + timedelta(weeks=4)).count()))
    p.drawString(40, 440, "Nombre d'actualités publiées lors de la dernière année : " + str(Actualite.objects.filter(date__lte=timezone.now() + timedelta(weeks=52)).count()))
    p.drawString(40, 425, "Nombre d'actualités publiées toutes périodes confondues : " + str(len(Actualite.objects.all())))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Rapport_SAD.pdf')
    
class RapportsAdmin(admin.ModelAdmin):
    model = Rapports
    
    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path2/', my_custom_view2, name=view_name),
        ]
admin.site.register(Rapports, RapportsAdmin)