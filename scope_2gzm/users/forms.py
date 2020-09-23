from django.forms import ModelForm
from .models import User

# Create the form class.
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'is_superuser', 'date_joined']
