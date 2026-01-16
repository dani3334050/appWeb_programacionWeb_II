import unittest
from app import create_app

class BasicApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health(self):
        resp = self.client.get('/api/health')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get('status'), 'ok')

    def test_protected_requires_jwt(self):
        # POST /api/vehicles ahora requiere JWT
        resp = self.client.post('/api/vehicles', json={})
        self.assertIn(resp.status_code, (401, 422))

if __name__ == '__main__':
    unittest.main()
