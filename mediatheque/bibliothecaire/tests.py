from django.test import TestCase, Client
from django.urls import reverse
from .models import Borrower, Book, Cd, Dvd, Borrow, Media
from django.utils.timezone import now


class CreateMemberTestCase(TestCase):
    def setUp(self):
        """
            Préparation des données valides et non valides pour créer un membre.
        """
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
        }
        self.invalid_data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'invalid-email',
        }

    def test_create_member_success(self):
        """
            Cette méthode va permettre de vérifier si la vue va traiter les données valides correctement.
            En premier lieu, une requête POST est envoyé à l'url de la vue et les données de formulaire sont transmises.

            Ensuite, on a une vérification sur le nombre de membres qui a été créée et si l'email correspond à celui des
            données valides.

            Enfin, la méthode vérifie qu'après la création du membre, l'utilisateur est redirigé vers le menu.
        """
        response = self.client.post(reverse('create_member_borrower'), data=self.valid_data)

        # Vérifiez que le membre a été créé
        self.assertEqual(Borrower.objects.count(), 1)
        self.assertEqual(Borrower.objects.first().email, 'johndoe@example.com')

        # Vérifiez la redirection
        self.assertRedirects(response, reverse('library_menu'))

class MembersListTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test : crée des membres pour tester l'affichage.
        """
        self.client = Client()
        self.url = reverse('members_list')

        # Création de membres fictifs
        Borrower.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        Borrower.objects.create(first_name="Jane", last_name="Smith", email="jane.smith@example.com")

    def test_members_list_success(self):
        """
        Teste que la liste des membres s'affiche correctement.

        Il envoie une requête HTTP GET vers l'url définie dans l'environnement et la réponse envoyé est stockée dans la
        variable response.

        Il vérifie que le code de statut est correcte. Ensuite, il vérifie que c'est bien le bon template qui est
        utilisé et vérifie que les noms des membres apparaissent dans le contenu HTML.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Jane Smith")

class UpdateMemberBorrowerTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test : en créant un membre existant. Une URL de la vue est générée pour le membre
        créé.
        """
        self.client = Client()
        self.member = Borrower.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        self.url = reverse('update_member_borrower', args=[self.member.id])

    def test_update_member_success(self):
        """
        Teste la mise à jour d'un membre avec des données valides.

        On commence par mettre une nouvelle valeur pour les attributs du membre. Une requête POST est envoyée à l'URL de
        mise à jour avec la nouvelle donnée.

        Il y a ensuite une vérification du code de statut et de la redirection.

        Enfin, il y a une vérification sur les données mise à jour en les rechargeant.
        """
        updated_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
        }

        response = self.client.post(self.url, updated_data)

        # Vérifie la redirection après mise à jour
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('members_list'))

        # Vérifie que les données ont été mises à jour
        self.member.refresh_from_db()
        self.assertEqual(self.member.first_name, 'John')
        self.assertEqual(self.member.last_name, 'Doe')
        self.assertEqual(self.member.email, 'johndoe@example.com')


class DeleteMemberBorrowerTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test : en créant un membre existant. Une URL de la vue est générée pour le membre
        créé.
        """
        self.client = Client()
        self.member = Borrower.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        self.url = reverse('delete_member_borrower', args=[self.member.id])

    def test_delete_member_success(self):
        """
        Teste la suppression d'un membre existant.

        Pour commencer, le test envoie une requête POST à l'URL pour faire la suppression.

        Ensuite, il vérifie que le code de statut est bon et que la redirection vers la liste des membres s'effectue.

        Enfin, le test vérifie que le membre supprimé n'existe plus dans la base de donnée.
        """
        response = self.client.post(self.url)

        # Vérifie que la redirection a eu lieu après suppression
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('members_list'))

        # Vérifie que le membre a été supprimé de la base de données
        with self.assertRaises(Borrower.DoesNotExist):
            Borrower.objects.get(id=self.member.id)

class MediaListTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test avec des livres, DVDs et CDs. Le client est utilisé pour envoyer des requêtes
        HTTP simulées et il utilise le nom de la vue pour générer l'URL.
        """
        self.client = Client()

        # Ajout de quelques médias
        self.book1 = Book.objects.create(name="Book 1", author="Author 1", available=True)
        self.book2 = Book.objects.create(name="Book 2", author="Author 2", available=False)
        self.dvd1 = Dvd.objects.create(name="DVD 1", director="Director 1", available=True)
        self.cd1 = Cd.objects.create(name="CD 1", artist="Artist 1", available=False)

        self.url = reverse('media_list')

    def test_media_list_view_success(self):
        """
        Teste si la vue renvoie correctement la liste des médias.

        Il commence par envoyer une requête GET à l'URL de la vue pour récupérer la liste des médias.

        Ensuite, il vérifie que la réponse a le bon code de statut.

        Enfin, il vérifie que les objets sont bien présent dans la réponse et donc qu'ils sont bien inclus dans les
        résultats renvoyés par la vue.
        """
        response = self.client.get(self.url)

        # Vérifie que la requête retourne un statut HTTP 200
        self.assertEqual(response.status_code, 200)

        # Vérifie que les objets sont bien dans le contexte
        self.assertContains(response, self.book1.name)
        self.assertContains(response, self.book2.name)
        self.assertContains(response, self.dvd1.name)
        self.assertContains(response, self.cd1.name)

class CreateBorrowTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test avec un emprunteur et des médias.
        """
        self.client = Client()

        # Création d'un emprunteur
        self.borrower = Borrower.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com"
        )

        # Création de médias
        self.media_available = Media.objects.create(name="Media Disponible", available=True)
        self.media_unavailable = Media.objects.create(name="Media Indisponible", available=False)

        # URL pour la vue create_borrow
        self.url = reverse('create_borrow', args=[self.borrower.id])

    def test_create_borrow_success(self):
        """
        Teste la création réussie d'un emprunt pour un média disponible.

        Pour commencer, le test simule une requête POST envoyé à l'URL pour créer un emprunt pour le média disponible.

        Ensuite, il vérifie que la réponse a le bon code de statut et que la redirection est bonne.

        Enfin, il vérifie que l'emprunt a bien été ajouté à la base de données pour le média et l'emprunteur.
        """
        response = self.client.post(self.url, {'media': self.media_available.id})

        # Vérifie que la redirection après la création de l'emprunt fonctionne
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('library_menu'))

        # Vérifie que l'emprunt a été créé
        self.assertTrue(Borrow.objects.filter(borrower=self.borrower, media=self.media_available).exists())
        borrow = Borrow.objects.get(borrower=self.borrower, media=self.media_available)
        self.assertEqual(borrow.media.name, "Media Disponible")
        self.assertEqual(borrow.media.available, False)

class AddBookTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test. Le client est utilisé pour envoyer des requêtes
        HTTP simulées et il utilise le nom de la vue pour générer l'URL.
        """
        self.client = Client()
        self.url = reverse('add_book')

    def test_add_book_success(self):
        """
        Teste l'ajout réussi d'un livre.

        Le test commence par simuler une requête POST à l'URL de la vue avec les données du formulaire.

        Ensuite, il vérifie que le code de statut est bon et que le livre a bien été ajouté à la base de données.
        """
        response = self.client.post(self.url, {
            'name': 'Test Book',
            'author': 'Test Author',
            'available': True,
        })

        # Vérifie que la redirection fonctionne après l'ajout
        self.assertEqual(response.status_code, 302)

        # Vérifie que le livre a été ajouté à la base de données
        self.assertTrue(Book.objects.filter(name='Test Book', author='Test Author').exists())

class AddCdTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test. Le client est utilisé pour envoyer des requêtes
        HTTP simulées et il utilise le nom de la vue pour générer l'URL.
        """
        self.client = Client()
        self.url = reverse('add_cd')

    def test_add_cd_success(self):
        """
        Teste l'ajout réussi d'un cd.

        Le test commence par simuler une requête POST à l'URL de la vue avec les données du formulaire.

        Ensuite, il vérifie que le code de statut est bon et que le cd a bien été ajouté à la base de données.
        """
        response = self.client.post(self.url, {
            'name': 'Test CD',
            'artist': 'Test Artist',
            'available': True,
        })

        # Vérifie que la redirection fonctionne après l'ajout
        self.assertEqual(response.status_code, 302)

        # Vérifie que le CD a été ajouté à la base de données
        self.assertTrue(Cd.objects.filter(name='Test CD', artist='Test Artist').exists())

class AddDvdTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test. Le client est utilisé pour envoyer des requêtes
        HTTP simulées et il utilise le nom de la vue pour générer l'URL.
        """
        self.client = Client()
        self.url = reverse('add_dvd')

    def test_add_dvd_success(self):
        """
        Teste l'ajout réussi d'un dvd.

        Le test commence par simuler une requête POST à l'URL de la vue avec les données du formulaire.

        Ensuite, il vérifie que le code de statut est bon et que le dvd a bien été ajouté à la base de données.
        """
        response = self.client.post(self.url, {
            'name': 'Test DVD',
            'director': 'Test Director',
            'available': True,
        })

        # Vérifie que la redirection fonctionne après l'ajout
        self.assertEqual(response.status_code, 302)

        # Vérifie que le DVD a été ajouté à la base de données
        self.assertTrue(Dvd.objects.filter(name='Test DVD', director='Test Director').exists())

class ReturnBorrowTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test avec un emprunt existant. Le client est utilisé pour envoyer des requêtes
        HTTP simulées. Ensuite, le média est marqué comme non disponible afin de simuler un emprunt. Puis, le test crée
        un emprunteur et l'associe au média. Enfin, le test utilise le nom de la vue pour générer l'URL.
        """
        self.client = Client()
        self.media = Media.objects.create(name="Test Media", available=False)
        self.borrower = Borrower.objects.create(
            first_name="John", last_name="Doe"
        )
        self.borrow = Borrow.objects.create(
            borrower=self.borrower,
            media=self.media,
            borrow_date=now(),
            is_returned=False
        )
        self.url = reverse('return_borrow', args=[self.borrow.id])

    def test_return_borrow_success(self):
        """
        Teste le retour réussi d'un emprunt.

        Elle commence par simuler une requête POST pour retourner l'emprunt. Puis, elle vérifie le statut et recharge
        les données borrow et media de la base de données pour s'assurer que les modifications effectuées par la vue
        sont visibles. Enfin, elle vérifie que l'attribut is_returned est marqué comme retourné, que la date de retour
        est définie et que le média est marqué comme disponible.
        """
        response = self.client.post(self.url)

        # Vérifie la redirection après le retour
        self.assertEqual(response.status_code, 302)

        # Rafraîchit les objets depuis la base de données
        self.borrow.refresh_from_db()
        self.media.refresh_from_db()

        # Vérifie que l'emprunt est marqué comme retourné
        self.assertTrue(self.borrow.is_returned)

        # Vérifie que la date de retour est définie
        self.assertIsNotNone(self.borrow.return_date)

        # Vérifie que le média est marqué comme disponible
        self.assertTrue(self.media.available)
