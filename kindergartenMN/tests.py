from django.test import TestCase, Client
from django.contrib.auth.models import User, Group

class RoleAccessTest(TestCase):
    def setUp(self):
        self.admin_group = Group.objects.create(name='Admin')
        self.chef_group = Group.objects.create(name='Chef')
        self.manager_group = Group.objects.create(name='Manager')
        self.admin = User.objects.create_user('admin', password='pass')
        self.chef = User.objects.create_user('chef', password='pass')
        self.manager = User.objects.create_user('manager', password='pass')
        self.admin.groups.add(self.admin_group)
        self.chef.groups.add(self.chef_group)
        self.manager.groups.add(self.manager_group)
        self.client = Client()

    def test_admin_access(self):
        self.client.login(username='admin', password='pass')
        resp = self.client.get('/api/users/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/api/inventory/notifications/')
        self.assertEqual(resp.status_code, 200)

    def test_chef_access(self):
        self.client.login(username='chef', password='pass')
        resp = self.client.get('/api/users/')
        self.assertEqual(resp.status_code, 403)
        resp = self.client.post('/api/meals/serve/', {'recipe_id': 1, 'portions': 1}, content_type='application/json')
        self.assertIn(resp.status_code, [200, 201, 400])  # 400 если нет данных

    def test_manager_access(self):
        self.client.login(username='manager', password='pass')
        resp = self.client.get('/api/users/')
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get('/api/inventory/notifications/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/api/meals/serve/', {'recipe_id': 1, 'portions': 1}, content_type='application/json')
        self.assertEqual(resp.status_code, 403) 