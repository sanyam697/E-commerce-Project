from django import forms
from .models import Contact, User

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class VisitorForm(forms.Form):
    email = forms.EmailField()

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput,label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    class Meta:
        model = User
        fields = ('fullname', 'email')

    def clean_password2(self):
        password1 =self.cleaned_data.get('password1')
        password2 =self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password must match")
        return password2

    def save(self,commit=True):
        user =super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields ="__all__"
