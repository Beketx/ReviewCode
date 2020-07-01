import pytest
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from main.models import Company
from main.models import Review
from rest_framework.authtoken.models import Token


class ReviewModelTest(TestCase):

    def test_is_possible_create_with_valid_parameters(self):
        company = Company.objects.create(name='Company 1', description='This is a test company')

        r = Review.objects.create(
            rating=1,
            title='My test review',
            summary='This is my test review with summary',
            ip_address='192.168.0.1',
            company=company,
            reviewer=Token.objects.create(user=User.objects.create_user(username='User1'))
        )
        self.assertEqual(r.title, 'My test review')
        self.assertEqual(r.company, company)

    def test_is_not_possible_create_without_company(self):
        with pytest.raises(IntegrityError, match="NOT NULL constraint failed: review_review.company_id"):
            Review.objects.create(
                rating=1,
                title='My test review',
                summary='This is my test review with summary',
                ip_address='192.168.0.1',
                reviewer=Token.objects.create(user=User.objects.create_user(username='User1'))
            )

    def test_if_can_get_all_reviews_from_one_user(self):
        company = Company.objects.create(name='Company 1', description='This is a test company')
        reviewer_1 = Token.objects.create(user=User.objects.create_user(username='User1'))
        reviewer_2 = Token.objects.create(user=User.objects.create_user(username='User2'))

        r1 = Review.objects.create(
            rating=1,
            title='My test review 1',
            summary='This is my test review with summary',
            ip_address='192.168.0.1',
            company=company,
            reviewer=reviewer_1
        )

        r2 = Review.objects.create(
            rating=2,
            title='My test review 2',
            summary='This is my test review with summary',
            ip_address='192.168.0.1',
            company=company,
            reviewer=reviewer_1
        )

        r3 = Review.objects.create(
            rating=3,
            title='My test review 3',
            summary='This is my test review with summary',
            ip_address='192.168.0.1',
            company=company,
            reviewer=reviewer_2
        )

        self.assertEqual(Review.objects.filter(reviewer=reviewer_1).count(), 2)
        self.assertEqual(Review.objects.filter(reviewer=reviewer_2).count(), 1)


class CompanyApiTests(APITestCase):

    def setUp(self):
        self.superuser1 = User.objects.create_superuser('john', 'john@snow.com', 'localpass1')
        self.superuser2 = User.objects.create_superuser('snow', 'snow@borne.com', 'localpass2')
        self.token1 = Token.objects.create(user=self.superuser1)
        self.client.login(username='john', password='localpass1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

    def test_can_get_all_companies(self):

        Company.objects.create(name='test', description='test description')

        response = self.client.get('/company/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_is_possible_create_review_for_a_new_company(self):

        response = self.client.post('/review/', format='json', data=
        {
            "rating": 1,
            "title": "asdf",
            "summary": "asdf",
            "company": {
                "name": "asdf",
                "description": "asdf"
            }
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
