from django.test import TestCase, Client
from bibliothecaire.models import Book, Dvd, Cd
from django.urls import reverse

class MediaListForMembersTestCase(TestCase):
    def setUp(self):
        """
        Prépare l'environnement de test avec des livres, DVDs et CDs. Le client est utilisé pour envoyer des requêtes
        HTTP simulées et il utilise le nom de la vue pour générer l'URL.
        """
        self.client = Client()

        # Crée des livres
        self.book1 = Book.objects.create(name="Book 1", author="Author 1", available=True)
        self.book2 = Book.objects.create(name="Book 2", author="Author 2", available=False)

        # Crée des DVDs
        self.dvd1 = Dvd.objects.create(name="DVD 1", director="Director 1", available=True)
        self.dvd2 = Dvd.objects.create(name="DVD 2", director="Director 2", available=False)

        # Crée des CDs
        self.cd1 = Cd.objects.create(name="CD 1", artist="Artist 1", available=True)
        self.cd2 = Cd.objects.create(name="CD 2", artist="Artist 2", available=False)

        # URL de la vue
        self.url = reverse('media_list_for_members')

    def test_media_list_view_status_code(self):
        """
        Teste que la vue renvoie un code 200 en envoyant une requête GET à l'URL de la vue.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_media_list_view_context(self):
        """
        Teste que la vue contient les bons médias dans le contexte.
        """
        response = self.client.get(self.url)

        # Vérifie la présence des objets dans le contexte
        self.assertIn(self.book1, response.context['books'])
        self.assertIn(self.book2, response.context['books'])
        self.assertIn(self.dvd1, response.context['dvds'])
        self.assertIn(self.dvd2, response.context['dvds'])
        self.assertIn(self.cd1, response.context['cds'])
        self.assertIn(self.cd2, response.context['cds'])

    def test_media_list_template_used(self):
        """
        Teste que la vue utilise le bon template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'media_list_for_members.html')