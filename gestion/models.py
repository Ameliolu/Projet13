from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    membre = models.CharField(max_length=1, null=True)
    newsletter = models.CharField(max_length=1, null=True)
    
class Cours(models.Model):
    date = models.DateField()
    heure = models.TimeField()
    adresse = models.TextField()
    texte_etudie = models.TextField()
    
    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

        
class Actualite(models.Model):
    nom = models.CharField(max_length=255)
    texte = models.TextField()
    image = models.ImageField(upload_to="photos/")
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        """
        le - devant date permet de faire ressortir par défaut
        les éléments par date descendante
        """
        ordering = ['-date']
    
    def __str__(self):
        return self.nom
