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
        quizer.app.config['DATA_FILE'] = 'data/test.csv'
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
        client = quizer.app.test_client()
        resp = client.post('/', data={'username': 'TEST'})
        resp = client.get('/pytanie')
        self.assertEqual(resp.status_code, 200)

        resp = client.post('/pytanie', data={'answer': 'A'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers['Location'].endswith('/pytanie'))

    def test_no_answers(self):
        """
        Checks result calculation when all ansers are empty.
        """
        resp = self.client.post('/', data={'username': 'TEST'})
        for i in range(6):
            resp = self.client.get('/pytanie')
            if i < 5:
                self.assertEqual(resp.status_code, 200)
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.headers['Location'].endswith('/wynik'))

        resp = self.client.get('/wynik')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('wynik to: 0/15 (0%)', resp.data)

    def test_max_points(self):
        """
        Checks result calculation when all ansers are correct.
        """
        resp = self.client.post('/', data={'username': 'TEST'})
        for i in range(5):
            resp = self.client.get('/pytanie')
            self.assertEqual(resp.status_code, 200)
            resp = self.client.post('/pytanie', data={'answer': 'A'})
            self.assertEqual(resp.status_code, 302)

            if i < 4:
                self.assertTrue(resp.headers['Location'].endswith('/pytanie'))
            else:
                self.assertTrue(resp.headers['Location'].endswith('/wynik'))

        resp = self.client.get('/wynik')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('wynik to: 15/15 (100%)', resp.data)


if __name__ == '__main__':
    unittest.main()
