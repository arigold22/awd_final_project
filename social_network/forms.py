from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    firstname = forms.CharField(label = "First name")
    lastname = forms.CharField(label = "Last name")

    class Meta:
        model = User
        fields = ("username", "firstname", "lastname", "email", )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        firstname = self.cleaned_data["firstname"]
        lastname = self.cleaned_data["lastname"]
        user.first_name = firstname
        user.last_name = lastname
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user