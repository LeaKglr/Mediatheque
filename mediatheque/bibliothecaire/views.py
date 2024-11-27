from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateMemberForm, BookForm, DvdForm, CdForm, BoardGameForm
from .models import Borrower, Book, Dvd, Cd, Borrow, Media, BoardGame
from django.contrib import messages
from django.utils.timezone import now
from django.utils import timezone
from django.db.models import Q
from django.core.management.base import BaseCommand
from datetime import timedelta

import logging

logger = logging.getLogger('mediatheque')

# Affiche le menu de l'application des bibliothécaires
def library_menu(request):
    logger.info("C'est le menu de l'application des bibliothécaires.")
    return render(request, 'library_menu.html')


# Première fonctionnalité : créer un membre-emprunteur
def create_member_borrower(request):
    """
        Cette méthode permet de soumettre un formulaire pour créer un nouveau membre-emprunteur.

        Il y a d'abord une vérification : si nous avons bien affaire à une soumission du formulaire (requête POST).
        Une instance du formulaire est créée en passant les données POST.
        Si le formulaire est valide, il y a une sauvegarde des données pour créer un objet Borrower puis un message de
        succès.

        On est ensuite renvoyé vers le menu de l'application des bibliothécaires.
        Si le formulaire est invalide, des logs apparaîssent dans la console pour le débogage.

        En revanche, si ce n'est pas une requête POST, mais une requête GET (sans données au préalable), il y a
        création d'un formulaire vide pour que l'utilisateur puisse le remplir. Puis, lorsque les champs sont remplis,
        on repart sur la requête POST comme vue ci-dessus avec la sauvegarde et la création d'un objet.


        Enfin, il y a une gestion des exceptions : si une erreur survient dans le bloc "try", les logs l'enregistrent,
        le bloc "except" la capture et la commande "raise" relance l'erreur afin que le reste de l'application sache
        qu'un problème est survenu.
    """
    try:
        logger.info("Début de la méthode create_member_borrower")

        if request.method == "POST":
            logger.info("Requête POST reçue pour créer un membre.")
            form = CreateMemberForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Le membre a été créé avec succès.")
                logger.info("Membre créé avec succès.")
                return redirect('library_menu')
            else:
                logger.warning("Le formulaire soumis est invalide.")
                logger.debug(f"Erreurs du formulaire : {form.errors}")
        else:
            logger.info("Requête GET reçue pour afficher le formulaire.")
            form = CreateMemberForm()

        return render(request, 'create_member.html', {'form': form})

    except Exception as e:
        logger.error(f"Erreur dans create_member_borrower : {str(e)}", exc_info=True)
        raise


# Deuxième fonctionnalité : afficher la liste des membres
def members_list(request):
    """
        Cette méthode permet d'afficher la liste des membres de la médiathèque.

        Elle commence par récupérer les objets Borrower de la base de données puis les stocke dans la variable members.

        Si tout est bien récupéré, le template members_list.html est affiché avec la liste des membres.
    """
    try:
        logger.info("Début de la méthode members_list")
        members = Borrower.objects.all()
        logger.debug(f"Nombre de membres récupérés : {members.count()}")
        return render(request, 'members_list.html', {'members': members})
    except Exception as e:
        logger.error(f"Erreur dans members_list : {str(e)}", exc_info=True)
        raise


# Troisième fonctionnalité : mettre à jour un membre
def update_member_borrower(request, member_id):
    """
        Cette méthode permet de mettre à jour un membre.

        Elle commence par récupérer un membre existant à partir de son ID. Si aucun membre ne correspond, une page
        d'erreur 404 s'affichera. Si le membre est trouvé, il est stocké dans la variable members.

        Ensuite, elle affiche un formulaire pré-rempli avec ses informations grâce à une requête POST.

        Puis, il y a une vérification de la validité des données et elle enregistre les modifications apportées à
        ce membre dans la base de données.
        Un message de succès s'affiche et redirige vers la liste des membres.

        Enfin, une gestion d'erreurs est faite.
    """
    logger.info(f"Tentative de mise à jour du membre avec ID {member_id}.")

    try:
        members = get_object_or_404(Borrower, id=member_id)
        logger.debug(f"Récupération réussie du membre : {members}.")

        if request.method == "POST":
            logger.info("Requête POST reçue pour la mise à jour.")
            form = CreateMemberForm(request.POST, instance=members)

            if form.is_valid():
                form.save()
                logger.info(f"Membre avec ID {member_id} mis à jour avec succès.")
                messages.success(request, "Le membre a été mis à jour avec succès.")
                return redirect('members_list')
            else:
                logger.warning("Le formulaire de mise à jour contient des erreurs.")
        else:
            logger.info("Requête GET reçue. Pré-remplissage du formulaire.")
            form = CreateMemberForm(instance=members)

        return render(request, 'update_member.html', {'form': form, 'members': members})

    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour du membre avec ID {member_id}: {str(e)}", exc_info=True)
        raise


# Quatrième fonctionnalité : supprimer un membre
def delete_member_borrower(request, member_id):
    """
        Cette méthode permet de supprimer un membre.

        Elle commence par récupérer un membre existant à partir de son ID. Si aucun membre ne correspond, une page
        d'erreur 404 s'affichera. Si le membre est trouvé, il est stocké dans la variable member.

        La méthode delete() est appelée afin de supprimer le membre.
        Ensuite, elle demande une confirmation avant la suppression.

        Puis, un message de succès est ajouté pour confirmer la suppression du membre et on est redirigé vers la liste
        des membres.

        Enfin, une gestion d'erreurs est faite.
    """
    logger.info(f"Tentative de suppression du membre avec ID {member_id}.")

    try:
        member = get_object_or_404(Borrower, id=member_id)
        logger.debug(f"Récupération réussie du membre : {member}.")

        if request.method == "POST":
            logger.info(f"Requête POST reçue. Suppression du membre avec ID {member_id}.")
            member.delete()
            logger.info(f"Membre avec ID {member_id} supprimé avec succès.")
            messages.success(request, "Le membre a été supprimé avec succès.")
            return redirect('members_list')
        else:
            logger.info(f"Requête GET reçue pour confirmer la suppression du membre avec ID {member_id}.")

        return render(request, 'delete_member.html', {'member': member})

    except Exception as e:
        logger.error(f"Erreur lors de la suppression du membre avec ID {member_id}: {str(e)}", exc_info=True)
        raise


# Cinquième fonctionnalité : afficher la liste des médias
def media_list(request):
    """
        Cette méthode permet d'afficher la liste des médias.

        Elle commence par récupérer tous les types de médias enregistrés dans la base de données pour les mettre chacun
        dans une variable correspondante. Puis, elle les affiche sur une page html : media_list.html.
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

    return render(request, 'media_list.html', {
        'books': books,
        'dvds': dvds,
        'cds': cds,
        'boardgames': boardgames,
    })


# Sixième fonctionnalité : créer un emprunt pour un média disponible
def create_borrow(request, member_id):
    """
        Cette méthode permet à un membre de la bibliothèque d'emprunter un média.

        Elle commence par récupérer le membre existant avec son ID. Si aucun membre ne correspond, une page
        d'erreur 404 s'affichera. Si le membre est trouvé, il est stocké dans la variable borrower.

        De plus, en sélectionnant le membre, elle va vérifier si le membre n'est pas bloqué, s'il n'a pas trois emprunts
        ou plus et s'il a des emprunts en retard.

        Lorsqu'on veut sélectionner le média, un filtrage est fait pour n'apercevoir que les médias disponibles.
        Ensuite, elle récupère le média sélectionné et l'enregistre. Il y a redirection vers le menu de l'application et
        un message de succès apparaît.

    """

    logger.info(f"Tentative d'emprunt de média par le membre avec ID {member_id}.")
    borrower = get_object_or_404(Borrower, id=member_id)

    # Vérification si l'emprunteur est bloqué
    if borrower.is_blocked:
        messages.error(request,
                       "Cet emprunteur est bloqué en raison d'emprunts en retard. Il ne peut pas emprunter de "
                       "nouveaux médias.")
        return redirect('members_list')

    # Vérifie si le membre n'a pas plus de 3 emprunts
    if borrower.active_borrows().count() >= 3:
        messages.error(request, "Ce membre a déjà atteint la limite de 3 emprunts actifs.")
        return redirect('members_list')

    # Vérifie si le membre a des emprunts en retard
    if borrower.has_overdue_borrow():
        messages.error(request, "Ce membre a un emprunt en retard et ne peut pas emprunter.")
        return redirect('members_list')

    if request.method == 'POST':
        logger.debug("Requête POST reçue pour emprunter un média.")

        media_id = request.POST.get('media')
        media = get_object_or_404(Media, id=media_id)
        logger.info(f"Média sélectionné : {media.name}, ID : {media.id}.")


        borrows = Borrow.objects.create(borrower=borrower, media=media, borrow_date=timezone.now())
        logger.info(f"Emprunt enregistré : {borrows}")

        media.available = False
        media.save()
        logger.info(f"Média {media.name} marqué comme non disponible.")

        messages.success(request, f'Le média "{media.name}" a été emprunté par {borrower.last_name} '
                                  f'{borrower.first_name}.')
        return redirect('library_menu')

    available_media = Media.objects.filter(available=True).exclude(Q(name__icontains='jeu de plateau'))

    logger.debug("Affichage du formulaire d'emprunt pour le membre.")

    return render(request, 'create_borrow.html', {
        'borrower': borrower,
        'media_list': available_media,
    })


# Septième fonctionnalité : ajouter un média
def add_book(request):
    """
        Cette méthode permet d'ajouter un média et plus particulièrement un livre.

        Il y a d'abord une vérification : si nous avons bien affaire à une soumission du formulaire (requête POST).
        Une instance du formulaire est créée en passant les données POST.
        Si le formulaire est valide, il y a une sauvegarde des données pour créer un objet Book puis un message de
        succès.

        En revanche, si ce n'est pas une requête POST, mais une requête GET (sans données au préalable), il y a
        création d'un formulaire vide pour que l'utilisateur puisse le remplir. Ensuite, lorsque les champs sont remplis,
        on repart sur la requête POST comme vue ci-dessus avec la sauvegarde et la création d'un objet.

        On est ensuite renvoyé vers le menu de l'application des bibliothécaires.
    """
    logger.info("Tentative d'ajout d'un livre.")

    if request.method == "POST":
        logger.debug("Requête POST reçue. Tentative de validation du formulaire.")
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            logger.info("Le formulaire est valide. Sauvegarde du livre.")
            book_form.save()
            messages.success(request, "Livre ajouté avec succès.")
            logger.info("Livre ajouté avec succès.")
            return redirect('library_menu')
        else:
            logger.warning("Le formulaire est invalide. Affichage d'un message d'erreur.")
            messages.error(request, "Erreur lors de l'ajout du livre.")
    else:
        logger.info("Requête GET reçue. Initialisation du formulaire vide.")
        book_form = BookForm()

    # Retourne le formulaire s'il ne s'agit pas d'une requête POST ou s'il est invalide
    return render(request, 'add_book.html', {'book_form': book_form})


def add_dvd(request):
    """
        Cette méthode permet d'ajouter un média et plus particulièrement un dvd.

        Il y a d'abord une vérification : si nous avons bien affaire à une soumission du formulaire (requête POST).
        Une instance du formulaire est créée en passant les données POST.
        Si le formulaire est valide, il y a une sauvegarde des données pour créer un objet Dvd puis un message de
        succès.

        En revanche, si ce n'est pas une requête POST, mais une requête GET (sans données au préalable), il y a
        création d'un formulaire vide pour que l'utilisateur puisse le remplir. Ensuite, lorsque les champs sont remplis,
        on repart sur la requête POST comme vue ci-dessus avec la sauvegarde et la création d'un objet.

        On est ensuite renvoyé vers le menu de l'application des bibliothécaires.
    """
    logger.info("Tentative d'ajout d'un dvd.")

    if request.method == "POST":
        logger.debug("Requête POST reçue. Tentative de validation du formulaire.")
        dvd_form = DvdForm(request.POST)

        if dvd_form.is_valid():
            logger.info("Le formulaire est valide. Sauvegarde du dvd.")
            dvd_form.save()
            messages.success(request, "Dvd ajouté avec succès.")
            logger.info("Dvd ajouté avec succès.")
            return redirect('library_menu')
        else:
            logger.warning("Le formulaire est invalide. Affichage d'un message d'erreur.")
            messages.error(request, "Erreur lors de l'ajout du dvd.")
    else:
        logger.info("Requête GET reçue. Initialisation du formulaire vide.")
        dvd_form = DvdForm()

    return render(request, 'add_dvd.html', {'dvd_form': dvd_form})


def add_cd(request):
    """
        Cette méthode permet d'ajouter un média et plus particulièrement un cd.

        Il y a d'abord une vérification : si nous avons bien affaire à une soumission du formulaire (requête POST).
        Une instance du formulaire est créée en passant les données POST.
        Si le formulaire est valide, il y a une sauvegarde des données pour créer un objet Cd puis un message de
        succès.

        En revanche, si ce n'est pas une requête POST, mais une requête GET (sans données au préalable), il y a
        création d'un formulaire vide pour que l'utilisateur puisse le remplir. Ensuite, lorsque les champs sont remplis,
        on repart sur la requête POST comme vue ci-dessus avec la sauvegarde et la création d'un objet.

        On est ensuite renvoyé vers le menu de l'application des bibliothécaires.
    """
    logger.info("Tentative d'ajout d'un cd.")

    if request.method == "POST":
        logger.debug("Requête POST reçue. Tentative de validation du formulaire.")
        cd_form = CdForm(request.POST)

        if cd_form.is_valid():
            logger.info("Le formulaire est valide. Sauvegarde du cd.")
            cd_form.save()
            messages.success(request, "Cd ajouté avec succès.")
            logger.info("Cd ajouté avec succès.")
            return redirect('library_menu')
        else:
            logger.warning("Le formulaire est invalide. Affichage d'un message d'erreur.")
            messages.error(request, "Erreur lors de l'ajout du cd.")
    else:
        logger.info("Requête GET reçue. Initialisation du formulaire vide.")
        cd_form = CdForm()
    return render(request, 'add_cd.html', {'cd_form': cd_form})


def add_boardgame(request):
    """
        Cette méthode permet d'ajouter un média et plus particulièrement un jeu de plateau.

        Il y a d'abord une vérification : si nous avons bien affaire à une soumission du formulaire (requête POST).
        Une instance du formulaire est créée en passant les données POST.
        Si le formulaire est valide, il y a une sauvegarde des données pour créer un objet jeu de plateau puis un
        message de succès.

        En revanche, si ce n'est pas une requête POST, mais une requête GET (sans données au préalable), il y a
        création d'un formulaire vide pour que l'utilisateur puisse le remplir. Ensuite, lorsque les champs sont remplis,
        on repart sur la requête POST comme vue ci-dessus avec la sauvegarde et la création d'un objet.

        On est ensuite renvoyé vers le menu de l'application des bibliothécaires.
    """
    logger.info("Tentative d'ajout d'un jeu de plateau.")

    if request.method == "POST":
        logger.debug("Requête POST reçue. Tentative de validation du formulaire.")
        boardgame_form = BoardGameForm(request.POST)

        if boardgame_form.is_valid():
            logger.info("Le formulaire est valide. Sauvegarde du jeu de plateau.")
            boardgame_form.save()
            messages.success(request, "Jeu de plateau ajouté avec succès.")
            logger.info("Jeu de plateau ajouté avec succès.")
            return redirect('library_menu')
        else:
            logger.warning("Le formulaire est invalide. Affichage d'un message d'erreur.")
            messages.error(request, "Erreur lors de l'ajout du jeu de plateau.")
    else:
        logger.info("Requête GET reçue. Initialisation du formulaire vide.")
        boardgame_form = BoardGameForm()
    return render(request, 'add_boardgame.html', {'boardgame_form': boardgame_form})

# Huitième fonctionnalité : rentrer un emprunt
def borrow_list(request):
    """
            Cette méthode permet d'afficher la liste des emprunts.

            Elle commence par récupérer les emprunts de la base de données puis elle les met dans une variable nommée
            "borrows". Ensuite, elle les affiche dans une liste grâce au template : borrow_list.html.

    """
    logger.info("Affichage de la liste des emprunts.")

    borrows = Borrow.objects.select_related('borrower', 'media')
    logger.debug(f"Nombre d'emprunts récupérés : {borrows.count()}")

    return render(request, 'borrow_list.html', {'borrows': borrows})

def return_borrow(request, borrow_id):
    """
        Cette méthode permet retourner un emprunt.

        Elle récupère l'emprunt qui a l'ID correspondant depuis la base de données. Elle marque l'emprunt comme retourné
        en changeant le champ à True. Elle enregistre la date de retour à la date actuelle puis sauvegarde les
        informations.
        De plus, elle fait une mise à jour de la disponibilité du média.
        Un retour à la liste des emprunts est fait.
    """
    try:
        logger.info(f"Tentative de retour de l'emprunt avec l'ID : {borrow_id}")

        borrow = get_object_or_404(Borrow, id=borrow_id)
        logger.debug(f"Emprunt trouvé : {borrow}")

        # Mise à jour de l'état de l'emprunt
        borrow.is_returned = True
        borrow.return_date = timezone.now().date()
        borrow.save()

        # Vérifier si l'emprunteur a encore des emprunts en retard
        if not borrow.borrower.has_overdue_borrow():
            borrow.borrower.is_blocked = False
            borrow.borrower.save()

        # Mise à jour de la disponibilité du média
        borrow.media.available = True
        borrow.media.save()

        logger.info(f"Emprunt avec l'ID {borrow_id} marqué comme retourné à la date {borrow.return_date}")
        messages.success(request, "Emprunt retourné avec succès.")
        return redirect('borrow_list')

    except Exception as e:
        logger.error(f"Erreur lors du retour de l'emprunt {borrow_id}: {str(e)}", exc_info=True)
        raise


# Neuvième fonctionnalité : un emprunt doit être retourné au bout d'une semaine
# et membre avec un retard ne peut plus emprunter
class Command(BaseCommand):
    """
        Cette méthode permet à un emprunt de ne pas dépasser une semaine et de bloquer un emprunteur s'il dépasse cette
        condition.

        La méthode va commencer par calculer la date de référence pour déterminer s'il y a des emprunts en retard.
        Puis, elle va afficher les informations en parcourant la liste des empruntés en retard.

    """
    help = 'Met à jour les emprunts en retard'

    def handle(self, *args, **kwargs):
        overdue_date = now() - timedelta(weeks=1)
        overdue_borrows = Borrow.objects.filter(is_returned=False, borrow_date__lt=overdue_date)

        for borrow in overdue_borrows:
            # Vérifie si l'emprunteur a des emprunts en retard
            borrower = borrow.borrower
            borrower.is_blocked = True
            borrower.save()  

            self.stdout.write(f"Emprunteur {borrower} est bloqué pour des emprunts en retard.")