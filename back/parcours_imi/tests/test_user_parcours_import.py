from io import StringIO

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from parcours_imi.admin.user_parcours_import import UserParcoursImportEntry, user_parcours_import, user_parcours_import_view

class UserParcoursImportViewTestCase(TestCase):
    fixtures = [
        'masters.json',

    ]

    def test_user_parcours_import_view(self):
        # Given
        students_to_import_csv = StringIO(
            'username,email,first_name,last_name,master\n'
            'louis.trezzini,louis.trezzini@eleves.enpc.fr,Louis,Trezzini,MVA\n'
            'clement.riu,clement.riu@eleves.enpc.fr,Clément,Riu,MVA\n'
        )

        # When
        client = Client()

        response = client.post(
            reverse('user_parcours_import'),
            dict(
                file=students_to_import_csv,
            ),
        )

        # Then
        self.assertLess(response.status_code, 400)
        self.assertIsNotNone(User.objects.get(username='louis.trezzini'))
        self.assertIsNotNone(User.objects.get(username='clement.riu'))

    def test_user_parcours_import(self):
        # Given
        students_to_import = [
            UserParcoursImportEntry(
                'louis.trezzini',
                'louis.trezzini@eleves.enpc.fr',
                'Louis',
                'Trezzini',
                'MVA',
            )
        ]

        # When
        user_parcours_import(students_to_import)

        # Then
        louist = User.objects.get(username='louis.trezzini')
        self.assertEqual(louist.first_name, 'Louis')
        self.assertEqual(louist.last_name, 'Trezzini')
        self.assertEqual(louist.parcours.master.short_name, 'MVA')
