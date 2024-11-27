from django.shortcuts import render
import logging

logger = logging.getLogger('mediatheque')

def menu(request):
    logger.info("Affichage de la page d'accueil de la médiathèque.")
    return render(request, 'menu.html')
