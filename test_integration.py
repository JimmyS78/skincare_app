import unittest
from flask_testing import TestCase
from app import create_app, db, Product

class TestIntegration(TestCase):

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

    def test_add_update_delete_product_flow(self):
        # Add a product
        response = self.client.post('/add', data=dict(
            name='Test Product',
            description='Test Description'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)

        # Update the added product
        product_id = Product.query.filter_by(name='Test Product').first().id
        response = self.client.post(f'/update_product/{product_id}', data=dict(
            name='Updated Product',
            description='Updated Description'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Product', response.data)

        # Delete the updated product
        response = self.client.get(f'/delete_product/{product_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Updated Product', response.data)

    def test_add_product_redirect_to_index(self):
        # Add a product and check if it redirects to the index page
        response = self.client.post('/add', data=dict(
            name='Test Product',
            description='Test Description'
        ), follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')

if __name__ == '__main__':
    unittest.main()
