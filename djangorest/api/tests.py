from django.test import TestCase
from .models import Bill
from datetime import date
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here


class ModelTestCase(TestCase):

    def setUp(self):
        self.bill_category = 'Car'
        self.bill_description = '上班'
        self.bill_amount = 15
        self.bill_date = date.today()
        user = User.objects.create(username='kitty')
        self.bill = Bill(
            category=self.bill_category,
            description=self.bill_description,
            amount=self.bill_amount,
            date=self.bill_date,
            owner=user)

    def test_model_can_create_a_bill(self):
        old_count = Bill.objects.count()
        self.bill.save()
        new_count = Bill.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='kitty')

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.bill_data = {
            'category': 'Car',
            'description': '上班',
            'amount': 15,
            'date': date.today(),
            'owner': user.id
            }
        self.response = self.client.post(
            reverse('create'),
            self.bill_data,
            fromat='json')

    def test_api_can_create_a_bill(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        new_client = APIClient()
        res = new_client.get(reverse('details', kwargs={'pk': 3}), format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_get_a_bill(self):
        bill = Bill.objects.get(id=1)
        response = self.client.get(
            reverse('details', kwargs={'pk': bill.id}),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bill)

    def test_api_can_update_bill(self):
        bill = Bill.objects.get()
        change_bill = {
            'category': 'Car',
            'description': '下班',
            'amount': 15,
            }
        res = self.client.put(
            reverse('details', kwargs={'pk': bill.id}),
            change_bill,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bill(self):
        bill = Bill.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': bill.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
