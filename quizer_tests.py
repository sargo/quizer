# -*- coding: utf-8 -*-
"""
Quizer - tests.
"""
import quizer
import unittest


class QuizerTestCase(unittest.TestCase):
    """
    Quizer application unittests.
    """

    def setUp(self):
        """
        Setup environment before each unittest.
        """
        quizer.app.config['TESTING'] = True
        self.client = quizer.app.test_client()

    def tearDown(self):
        """
        Clean environment after unittest.
        """
        del quizer.app.config['TESTING']

    def test_welcome_page(self):
        """
        Checks is username input field on welcome page.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Quizer</h1>', resp.data)
        self.assertIn('<input type="text" name="username" />', resp.data)
        self.assertNotIn('Pole nie może być puste!', resp.data)

    def test_welcome_page_empty_username(self):
        """
        Checks validation of username input field.
        """
        resp = self.client.post('/', data={'username': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<input type="text" name="username" />', resp.data)
        self.assertIn('Pole nie może być puste!', resp.data)

    def test_welcome_page_start(self):
        """
        Checks redirect to first question after submit of username.
        """
        username = 'TEST'
        resp = self.client.post('/', data={'username': username})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers['Location'].endswith('/pytanie'))

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<p>Witaj, {0}</p>'.format(username), resp.data)

    def test_question_page(self):
        """
        Checks question page.
        """
        resp = self.client.get('/pytanie')
        self.assertEqual(resp.status_code, 200)

    def test_result_page(self):
        """
        Checks result page.
        """
        resp = self.client.get('/wynik')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
