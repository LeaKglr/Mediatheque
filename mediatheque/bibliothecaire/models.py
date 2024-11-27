from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone


class Media(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Media')
    loanDate = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)
    borrower = models.ForeignKey('Borrower', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Media"

    def __str__(self):
        return f"{self.name} - {'Disponible' if self.available else 'Non disponible'}"

class Book(Media):
    author = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.name} - {self.author}"

class Dvd(Media):
    director = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "DVDs"

    def __str__(self):
        return f"{self.name} - {self.director}"

class Cd(Media):
    artist = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "CDs"

    def __str__(self):
        return f"{self.name} - {self.artist}"


class BoardGame(models.Model):
    nameGame = models.CharField(max_length=50)
    creator = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "BoardGames"

    def __str__(self):
        return f"{self.nameGame} - {self.creator}"

class Borrower(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    def active_borrows(self):
        """Retourne les emprunts actifs."""
        return self.borrow_set.filter(is_returned=False)

    def has_overdue_borrow(self):
        """Vérifie si ce membre a un emprunt en retard."""
        overdue_date = now() - timedelta(weeks=1)
        return self.borrow_set.filter(is_returned=False, borrow_date__lt=overdue_date).exists()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Borrow(models.Model):
    borrower = models.ForeignKey('Borrower', on_delete=models.CASCADE)
    media = models.ForeignKey('Media', on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower} - {self.media} (Emprunté le {self.borrow_date})"

    def has_overdue_borrow(self):
        """
        Vérifie si l'emprunteur a des emprunts en retard.
        """
        overdue_borrows = self.borrow_set.filter(is_returned=False, borrow_date__lt=timezone.now() - timedelta(weeks=1))
        return overdue_borrows.exists()