from django.test import TestCase
from django.contrib.auth.models import User

from parcours_imi.admin import user_parcours_import_view

class UserParcoursImportViewTestCase(TestCase):
    fixtures = [
        'masters.json',
    ]

    def setUp(self):
        pass

    def test_users_are_imported(self):
        # Given

        # When
        user_parcours_import_view(None)

        # Then
        louist = User.objects.get(username='louis.trezzini')
        self.assertEqual('Louis', louist.first_name)
        self.assertEqual('Trezzini', louist.last_name)
        self.assertEqual('MVA', louist.parcours.master.short_name)
