from django.shortcuts import render
from bibliothecaire.models import Book, Dvd, Cd, BoardGame

import logging

logger = logging.getLogger('mediatheque')


def member_menu(request):
    logger.info("C'est le menu de l'application des membres.")
    return render(request, 'member_menu.html')


def media_list_for_members(request):
    """
        Cette méthode permet d'afficher la liste des médias.

        Elle commence par récupérer tous les types de médias enregistrés dans la base de données pour les mettre chacun
        dans une variable correspondante. Puis, elle les affiche sur une page html : media_list_for_members.html.
    """
    try:
        books = Book.objects.all()
        dvds = Dvd.objects.all()
        cds = Cd.objects.all()
        boardgames = BoardGame.objects.all()
        logger.debug(f"Nombre de livres : {books.count()}, DVDs : {dvds.count()}, CDs : {cds.count()}, "
                     f"BoardGames : {boardgames.count()}")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des médias : {str(e)}")
        books, dvds, cds, boardgames = [], [], [], []

    return render(request, 'media_list_for_members.html', {
        'books': books,
        'dvds': dvds,
        'cds': cds,
        'boardgames': boardgames,
    })



