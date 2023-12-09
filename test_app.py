import unittest
from app import create_app, db, Product

class TestApp(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.application.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_product(self):
        response = self.app.post('/add', data=dict(name='Test Product', description='Test Description'))
        self.assertEqual(response.status_code, 302)  # 302 means a redirect
        products = Product.query.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, 'Test Product')
        self.assertEqual(products[0].description, 'Test Description')

    def test_update_product(self):
        product = Product(name='Original Name', description='Original Description')
        with self.app.application.app_context():
            db.session.add(product)
            db.session.commit()

        response = self.app.post(f'/update_product/{product.id}', data=dict(name='Updated Name', description='Updated Description'))
        self.assertEqual(response.status_code, 302)
        updated_product = Product.query.get(product.id)
        self.assertEqual(updated_product.name, 'Updated Name')
        self.assertEqual(updated_product.description, 'Updated Description')

    def test_delete_product(self):
        product = Product(name='To Be Deleted', description='Delete This')
        with self.app.application.app_context():
            db.session.add(product)
            db.session.commit()

        response = self.app.get(f'/delete_product/{product.id}')
        self.assertEqual(response.status_code, 302)
        deleted_product = Product.query.get(product.id)
        self.assertIsNone(deleted_product)

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # 200 means success
        # You may want to add more detailed checks based on your actual index.html template

if __name__ == '__main__':
    unittest.main()

