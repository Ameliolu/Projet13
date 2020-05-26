from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Cours, Actualite, CustomUser

def home(request):
    modal = False
            
    if request.method == 'POST':
        email = request.POST.get('email')
        new, created = CustomUser.objects.update_or_create(email=email, defaults={'newsletter': 'o'})
        if created == True:
            nb_newsletter = len(CustomUser.objects.filter(username__icontains='Inscrit Newsletter')) + 1
            new.username = "Inscrit Newsletter n° " + str(nb_newsletter)
            new.save()
        modal = True

    """
    la requête fonctionne en 3 étapes :
    - filtrage des dates inférieures à la date actuelle
    - on trie les dates obtenus par ordre ascendant
    - on récupère la première date
    """
    prochaine_date = Cours.objects.filter(date__gte=timezone.now()).order_by('date')[:1]
    return render(
        request,
        'accueil.html',
        {'cours': prochaine_date,
        'modal' : modal}
    )
    
def actualite(request):
    return render(
        request, 
        'actualite.html', 
        {'actualites': Actualite.objects.all()}
    )
    
def legal(request):
    return render(request, 'legal.html')
    
def contact(request):
    return render(request, 'contact.html')