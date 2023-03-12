from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Post

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
    
class PostForm(forms.ModelForm):
    text = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'What\'s on your mind?', 'onchange': 'character_count()', 'onkeypress': 'character_count()', 'onfocus': 'character_count()' ,'oninput': 'character_count()', 'onkeyup':'character_count()','onpaste':'character_count()'}))
    images = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'multiple': True, 'onchange': 'previewImages(this)'}))
    class Meta:
        model = Post
        fields = ("text", )

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Type something or someone to search for ...'}))

class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    profile_image = forms.ImageField(required=False)
    remove_profile_image = forms.BooleanField(required=False)
    profile_cover_photo = forms.ImageField(required=False)
    remove_cover_photo = forms.BooleanField(required=False)
    profile_bio = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'placeholder': 'Write something about yourself ...'}))