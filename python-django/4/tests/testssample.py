from unittest import TestCase

from django.apps import apps


class TestAll(TestCase):
    def test_custom_user_creation(self):
        CustomUser = apps.get_model('users_app', 'CustomUser')
        
        user = CustomUser.objects.create(
            username='john.doe',
            email='john.doe@example.com',
            first_name='John',
            last_name='Doe',
            phone='+1234567890',
            national_id='ID001',
            address='123 Main Street',
            user_type='customer',
            status='active'
        )
        
        self.assertEqual(user.username, 'john.doe')
        self.assertEqual(user.email, 'john.doe@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.phone, '+1234567890')
        self.assertEqual(user.national_id, 'ID001')
        self.assertEqual(user.user_type, 'customer')
        self.assertEqual(user.status, 'active')
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertEqual(user.full_name, 'John Doe')

    def test_admin_user_with_profile(self):
        CustomUser = apps.get_model('users_app', 'CustomUser')
        AdminProfile = apps.get_model('users_app', 'AdminProfile')
        
        admin_user = CustomUser.objects.create(
            username='admin.user',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            phone='+1234567891',
            national_id='ADM001',
            address='456 Admin Street',
            user_type='admin',
            status='active'
        )
        
        admin_profile = AdminProfile.objects.create(
            user=admin_user,
            admin_code='ADM001',
            permissions={'can_manage_users': True, 'can_manage_products': True}
        )
        
        self.assertEqual(admin_user.user_type, 'admin')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        
        self.assertEqual(admin_profile.user, admin_user)
        self.assertEqual(admin_profile.admin_code, 'ADM001')
        self.assertEqual(admin_profile.permissions, {'can_manage_users': True, 'can_manage_products': True})
        self.assertIsNotNone(admin_profile.created_at)
        self.assertIsNotNone(admin_profile.updated_at)
        self.assertEqual(str(admin_profile), 'Admin Profile - Admin User')

    def test_user_status_choices(self):
        CustomUser = apps.get_model('users_app', 'CustomUser')
        
        active_user = CustomUser.objects.create(
            username='active.user',
            email='active@example.com',
            first_name='Active',
            last_name='User',
            phone='+1234567892',
            national_id='ACT001',
            address='789 Active Street',
            user_type='customer',
            status='active'
        )
        
        inactive_user = CustomUser.objects.create(
            username='inactive.user',
            email='inactive@example.com',
            first_name='Inactive',
            last_name='User',
            phone='+1234567893',
            national_id='INACT001',
            address='321 Inactive Street',
            user_type='customer',
            status='inactive'
        )
        
        suspended_user = CustomUser.objects.create(
            username='suspended.user',
            email='suspended@example.com',
            first_name='Suspended',
            last_name='User',
            phone='+1234567894',
            national_id='SUSP001',
            address='654 Suspended Street',
            user_type='customer',
            status='suspended'
        )
        
        self.assertEqual(active_user.status, 'active')
        self.assertEqual(inactive_user.status, 'inactive')
        self.assertEqual(suspended_user.status, 'suspended')