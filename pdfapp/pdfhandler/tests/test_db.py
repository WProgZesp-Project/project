from django.test import TestCase
from pdfhandler.models import TestModel

class AddModelTestCase(TestCase):
    def test_create_model(self):
        my_test_model = TestModel(name='test')
        my_test_model.save()
        self.assertEqual(TestModel.objects.count(), 1)