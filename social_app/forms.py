from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, label=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Your Password'
    }))
    password2 = forms.CharField(max_length=20, label=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter The Repeat Password '
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']

        widgets = {
            'username': forms.TextInput(attrs={

                'placeholder': 'Enter Your Username'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter Your First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter Your Last Name'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Enter Your Email'
            })
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError("Passwords do not match")
        return cd['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone Already Exists")
        elif phone[:2] != "09":
            raise forms.ValidationError("Phone Must Start With '09'")
        else:
            return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username Already Exists")
        else:
            return username


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'job', 'photo', 'phone']


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("BG", "bug"),
        ("PR", "proposal"),
        ("CR", "critics"),
    )

    body = forms.CharField(widget=forms.Textarea, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)


class AddPostForm(forms.ModelForm):
    image = forms.ImageField(label='post image', required=False)
    add_or_not = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            del self.fields['add_or_not']

    class Meta:
        model = Post
        fields = ["discription", "tags"]
        widgets = {
            'discription': forms.Textarea
        }

    def clean_add(self):
        cd = self.cleaned_data
        if not cd['add']:
            same_images = PostsImage.objects.filter(post__discription=cd["discription"]).exclude(image=cd["image"])
            for i in same_images:
                i.delete()


class SearchForm(forms.Form):
    query = forms.CharField()


class CommentForm(forms.Form):
    author = forms.CharField(max_length=20, required=False)
    text = forms.CharField(widget=forms.Textarea, required=True)
