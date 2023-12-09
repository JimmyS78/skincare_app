import unittest
from flask_testing import TestCase
from app import create_app, db, Product

class TestApp(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_product(self):
        response = self.client.post('/add', data=dict(
            name='Test Product',
            description='Test Description'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)

    def test_update_product(self):
        product = Product(name='Test Product', description='Test Description')
        db.session.add(product)
        db.session.commit()

        response = self.client.post(f'/update_product/{product.id}', data=dict(
            name='Updated Product',
            description='Updated Description'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Product', response.data)

    def test_delete_product(self):
        product = Product(name='Test Product', description='Test Description')
        db.session.add(product)
        db.session.commit()

        response = self.client.get(f'/delete_product/{product.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Product', response.data)

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Skincare Heaven', response.data)

if __name__ == '__main__':
    unittest.main()
