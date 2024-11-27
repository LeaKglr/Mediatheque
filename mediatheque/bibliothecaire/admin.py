from django.contrib import admin
from .models import Media, Book, Dvd, Cd, BoardGame, Borrower

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'loanDate', 'available')
    search_fields = ('name', 'author')

@admin.register(Dvd)
class DvdAdmin(admin.ModelAdmin):
    list_display = ('name', 'director', 'loanDate', 'available')
    search_fields = ('name', 'director')

@admin.register(Cd)
class CdAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'loanDate', 'available')
    search_fields = ('name', 'artist')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'loanDate', 'available')
    search_fields = ('name',)

# Admin pour BoardGame
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ('nameGame', 'creator')
    search_fields = ('nameGame',)
    list_filter = ('creator',)
    ordering = ('nameGame',)


# Admin pour Borrower
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'registration_date')
    search_fields = ('last_name', 'first_name', 'email')
    list_filter = ('registration_date',)
    ordering = ('last_name',)


# Enregistrement des modèles dans l'admin
admin.site.register(BoardGame, BoardGameAdmin)
admin.site.register(Borrower, BorrowerAdmin)
