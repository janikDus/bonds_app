from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json

class BondsTests(APITestCase):

    def test_create_bond(self):
        """Ensure we can create a new bond object."""

        url = reverse('post_bonds')
        data = {"bond_name": "Test", 'isin': 'CZ0003509507', "bond_value": 1, "interest_rate": 0.01, "purchase_date": "2023-01-01T01:00:00Z", "due_date": "2026-01-01T01:00:00Z", "yields_freq": 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_show_bond(self):
        """Ensure we can view all bond objects."""

        url = reverse('post_bonds')
        data = {"bond_name": "Test2", 'isin': 'CZ0003509507', "bond_value": 2, "interest_rate": 0.02, "purchase_date": "2023-02-01T01:00:00Z", "due_date": "2026-02-01T01:00:00Z", "yields_freq": 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('view_bonds')
        response = self.client.get(url)
        self.assertIsInstance(json.loads(response.content)['Bonds'], list)
    
    def test_manage_bond(self):
        """Ensure we can manage bond objects."""

        isin = 'CZ0003509507'

        url = reverse('post_bonds')
        data = {"bond_name": "Test3", 'isin': isin, "bond_value": 3, "interest_rate": 0.03, "purchase_date": "2023-03-01T01:00:00Z", "due_date": "2026-03-01T01:00:00Z", "yields_freq": 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('manage_bond', args=[isin])
        response = self.client.get(url)
        self.assertIsInstance(json.loads(response.content)['Bond'], dict)

        data = {"bond_name": "Test3_UPDATED", 'isin': isin, "bond_value": 3, "interest_rate": 0.03, "purchase_date": "2023-03-01T01:00:00Z", "due_date": "2026-03-01T01:00:00Z", "yields_freq": 3}
        url = reverse('manage_bond', args=[isin])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(json.loads(response.content)['bond_name'], "Test3_UPDATED")

        url = reverse('manage_bond', args=[isin])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_bonds_statistics(self):
        """Ensure we can analyze bond objects."""

        url = reverse('post_bonds')
        data = {"bond_name": "Test1", 'isin': 'CZ0003509507', "bond_value": 10, "interest_rate": 0.1, "purchase_date": "2023-03-01T01:00:00Z", "due_date": "2026-03-01T01:00:00Z", "yields_freq": 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('post_bonds')
        data = {"bond_name": "Test2", 'isin': 'CZ0005133611', "bond_value": 90, "interest_rate": 0.9, "purchase_date": "2023-03-01T01:00:00Z", "due_date": "2026-03-01T01:00:00Z", "yields_freq": 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('bond_analyzer')
        response = self.client.get(url)
        self.assertIsInstance(json.loads(response.content)['Statistic'], dict)
        self.assertEqual(json.loads(response.content)['Statistic']['avg_interest_rate'], 0.5)


        
