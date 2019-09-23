from io import StringIO

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from parcours_imi.admin.user_parcours_export import user_parcours_export_view

class UserParcoursExportViewTestCase(TestCase):
    fixtures = [
        'options.json',
        'masters.json',
        'constraints.json',
    ]

    def test_user_parcours_export_view(self):
        # Given
        students_to_import_csv = StringIO(
            'username;email;first_name;last_name;master\n'
            'louis.trezzini;louis.trezzini@eleves.enpc.fr;Louis;Trezzini;MVA\n'
            'clement.riu;clement.riu@eleves.enpc.fr;Clément;Riu;MVA\n'
        )

        # When
        client = Client()

        response = client.post(
            reverse('user_parcours_export'),
        )

        # Then
        self.assertLess(response.status_code, 400)
        self.assertEqual("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", response['Content-Type'])
