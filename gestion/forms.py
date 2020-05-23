from django import forms

CATEGORIE_DESTINATAIRES = [
    ('membres', 'Membres'),
    ('newsletter', 'Newsletter'),
]
        
class CourrielForm(forms.Form):
    Titre = forms.CharField(max_length=100)
    Texte = forms.CharField(widget=forms.Textarea)
    Destinataires = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=CATEGORIE_DESTINATAIRES,
    )
    
    