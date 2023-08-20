from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, label='Username', )
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    email = forms.EmailField(label='email')
    first_name = forms.CharField(max_length=100, label="first name")
    last_name = forms.CharField(max_length=100, label="last name")
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            SignupForm.add_error(self, field='confirm_password', error='Passwords do not match.')
            raise forms.ValidationError('Passwords do not match.')
