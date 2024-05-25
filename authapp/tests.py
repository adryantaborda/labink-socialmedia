from django.test import TestCase
from .models import User
from .forms import MyUserCreationForm

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username = 'Joe',email = 'joe123@gmail.com',password = '4cjdea',gender = 'MALE',birthday = '1023-02-23')
    
    def test_user_is_valid(self):
        user = User.objects.get(username = 'Joe')
        self.assertTrue(user.gender in User.genders)
        self.assertTrue('@' in user.email)
        self.assertTrue(len(user.password) >= 6)