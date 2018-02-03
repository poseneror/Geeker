from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from Geeker.models import User, Ticket
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from phonenumber_field.modelfields import PhoneNumberField


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.widgets.TextInput, label="Email")
    password1 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label="Password (again)")
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'date_of_birth', 'first_name', 'last_name', 'field', 'info',
                  'website', 'image', 'is_supplier']
    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    """
    def clean(self):
        cleaned_data = super(ProfileCreationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(ProfileCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user"""


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth', 'first_name', 'last_name', 'website', 'image')

    def clean_password(self):
        return self.initial["password"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('review_text', 'review_rating')


class RequestForm(forms.ModelForm):
    name = forms.CharField(label="your name")
    email = forms.EmailField(label="yourmail@domain.com")
    title = forms.CharField(label="what is the problem?")
    class Meta:
        model = Ticket
        fields = ('name', 'email', 'phone', 'title', 'description')


class AssignForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields =('assigned',)