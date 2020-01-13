import unittest
import json
from base64 import b64encode
from app import create_app, db


class UsersTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.users_route = '/v1/users/'
        self.token_route = '/v1/token/'
        
        self.user = {
            'id': '1',
            'email': 'max@example.com',
            'password_hash': '12345',
            'name': 'Max'
        }


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def get_headers_auth_basic(self, email, password_hash):
        return {
            'Authorization': 'Basic ' + b64encode(
                (email + ':' + password_hash).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }


    def get_headers_auth_token(self, token):
        return {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }


    def test_user_flow(self):
        # create a user (POST)
        response = self.client.post(
            self.users_route,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(self.user)
        )
        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.get_data(as_text=True))
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # get a token (POST)
        response = self.client.post(
            self.token_route,
            headers=self.get_headers_auth_basic(
                self.user['email'],
                self.user['password_hash']
            )
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # get users (GET)
        response = self.client.get(
            self.users_route,
            headers=self.get_headers_auth_token(token)
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('_links'))

        # get a specific user (GET)
        response = self.client.get(
            self.users_route + self.user['id'],
            headers=self.get_headers_auth_token(token)
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['email'], 'max@example.com')

        # modify a user (PUT)
        response = self.client.put(
            self.users_route + self.user['id'],
            headers=self.get_headers_auth_token(token),
            data=json.dumps({'name': 'Maximillion'})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'Maximillion')

        # delete a user (DELETE)
        response = self.client.delete(
            self.users_route + self.user['id'],
            headers=self.get_headers_auth_token(token),
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'the user has been deleted!')


if __name__ == '__main__':
    unittest.main()