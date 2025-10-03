# from django.test import TestCase
# # Create your tests here.
# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework import status
# from .models import Problem


# class ProblemAPITest(APITestCase):
# 	def test_create_and_list_problem(self):
# 		url = reverse('problem-list')
# 		data = {
# 			'title': 'Two Sum',
# 			'description': 'Find two numbers that add up to target',
# 			'difficulty': 'Easy',
# 			'deep_link': 'https://example.com/two-sum',
# 			'solved': False,
# 		}
# 		# create
# 		resp = self.client.post(url, data, format='json')
# 		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
# 		# list
# 		resp = self.client.get(url, format='json')
# 		self.assertEqual(resp.status_code, status.HTTP_200_OK)
# 		self.assertTrue(len(resp.data) >= 1)
# # Create your tests here.
