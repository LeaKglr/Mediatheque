from django import forms
from .models import Book, Dvd, Cd, Borrower, BoardGame

class CreateMemberForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['last_name', 'first_name', 'email']

# Formulaire pour Book
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'loanDate', 'available', 'borrower', 'author']

# Formulaire pour Dvd
class DvdForm(forms.ModelForm):
    class Meta:
        model = Dvd
        fields = ['name', 'loanDate', 'available', 'borrower', 'director']

# Formulaire pour Cd
class CdForm(forms.ModelForm):
    class Meta:
        model = Cd
        fields = ['name', 'loanDate', 'available', 'borrower', 'artist']

# Formulaire pour jeu de plateau
class BoardGameForm(forms.ModelForm):
    class Meta :
        model = BoardGame
        fields = ['nameGame', 'creator']