import pytest
from datetime import date
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import exceptions
from universities.models import ConsumerUnit

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils
from users.requests_permissions import RequestsPermissions

TOKEN_ENDPOINT = '/api/token/'
ENDPOINT_UNIVERSITY = '/api/universities/'

ENDPOINT = '/api/users/'
ENDPOINT_USER_UNIVERSITY = '/api/university-user/'

@pytest.mark.django_db
class TestRequestPermissions:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)
        self.super_user_dict = dicts_test_utils.super_user_dict_1
        self.super_user = create_objects_test_utils.create_test_super_user(self.super_user_dict)
        self.nonexisting_user = create_objects_test_utils.create_test_nonuniversity_user(self.nonexisting_user)
        self.client = APIClient()
        self.client.login(
            email = self.super_user_dict['email'], 
            password = self.super_user_dict['password'])

        self.consumer_units = []
        for i in range(3):
            self.consumer_units.append(ConsumerUnit(
                id=i+1,
                name=f'UC {i+1}',
                code=f'{i+1}',
                university=self.university,
                is_active=True,
                created_on=date.today()
            ))
        ConsumerUnit.objects.bulk_create(self.consumer_units)
    
    def test_check_request_permissions_user_without_permissions(self):
        with self.assertRaises(exceptions.AuthenticationFailed) as context:
            RequestsPermissions.check_request_permissions(self.nonexisting_user, type(self.nonexisting_user))
        
        self.assertEqual(str(context.exception), "This User does not have permission.")

    def test_check_request_permissions_user_with_permissions_but_no_id(self):
        
        with self.assertRaises(exceptions.AuthenticationFailed) as context:
            RequestsPermissions.check_request_permissions(self.user, type(self.user))
        
        self.assertEqual(str(context.exception), "University id is necessary.")
        