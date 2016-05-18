from .models import Guest
from django import forms
from django.contrib import messages

class GuestForm(forms.ModelForm):
	"""
	Registration form
	"""
	class Meta:
		model = Guest
		fields = [
			'name',
			'surname',
			'email',
			'guest_password',
			'repeat_guest_password',
		]

	#pomocu ovog dole moguce je primenjivati razlicite nacine za styling nasih polja odradjenih preko djanga
	def __init__(self, *args, **kwargs):
		super(GuestForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget = forms.TextInput(attrs={
			'placeholder': 'Name*',
			'required': True,
			'class': "form-first-name form-control"
			})

		self.fields['surname'].widget = forms.TextInput(attrs={
			'placeholder': 'Surname*',
			'required': True,
			'class': "form-last-name form-control"
			})

		self.fields['email'].widget = forms.EmailInput(attrs={
			'placeholder': 'Email*',
			'required': True,
			'class': "form-email form-control"
			})

		self.fields['guest_password'].widget = forms.PasswordInput(attrs={
			'placeholder': 'Enter password*',
			'required': True,
			'class': "form-first-name form-control"
			})

		self.fields['repeat_guest_password'].widget = forms.PasswordInput(attrs={
			'placeholder': 'Confirm password*',
			'required': True,
			'class': "form-first-name form-control"
			})

class AuthenticationForm(forms.Form):
	"""
	Login form
	"""

	email_address = forms.CharField(widget = forms.EmailInput(attrs={
		'placeholder': 'Email*',
		'required': True,
		'class': "form-email form-control"
	}))

	password = forms.CharField(widget = forms.PasswordInput(attrs={
			'placeholder': 'Password*',
			'required': True,
			'class': "form-first-name form-control"
			}))



	# class Meta:
	# 	model = Guest
	# 	fields = [
	# 		'email',
	# 		'guest_password'
	# 		]


	# def __init__(self, *args, **kwargs):
	# 	super(AuthenticationForm, self).__init__(*args, **kwargs)
	# 	self.fields['email'].widget = forms.EmailInput(attrs={
	# 		'placeholder': 'Email*',
	# 		'required': True,
	# 		'class': "form-email form-control"
	# 		})
	#
	# 	self.fields['guest_password'].widget = forms.PasswordInput(attrs={
	# 		'placeholder': 'Password*',
	# 		'required': True,
	# 		'class': "form-first-name form-control"
	# 		})

class UpdateGuestProfileForm(forms.ModelForm):
	"""
	Forma za izmenu podataka gosta
	"""

	class Meta:
		model = Guest
		fields = ['email', 'name', 'surname', 'profile_picture']

	def __init__(self, *args, **kwargs):
		super(UpdateGuestProfileForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget = forms.EmailInput(attrs={
			'placeholder': 'Email*',
			'required': True,
			'class': "form-control"
			})

		self.fields['name'].widget = forms.TextInput(attrs={
			'placeholder': 'Name*',
			'required': True,
			'class': "form-control"
			})

		self.fields['surname'].widget = forms.TextInput(attrs={
			'placeholder': 'Surname*',
			'required': True,
			'class': "form-control"
			})

class ChangeGuestPasswordForm(forms.ModelForm):
	"""
	Forma za izmenu lozinke
	"""

	current_password = forms.CharField(required = True, max_length = 50)

	class Meta:
		model = Guest
		fields = ['guest_password', 'repeat_guest_password', 'current_password']

	def __init__(self, *args, **kwargs):
		super(ChangeGuestPasswordForm, self).__init__(*args, **kwargs)
		self.fields['guest_password'].widget = forms.PasswordInput(attrs={
			'placeholder': 'Unesite novu lozinku*',
			'required': True,
			'class': "form-control"
			})

		self.fields['repeat_guest_password'].widget = forms.PasswordInput(attrs={
			'placeholder': 'Ponovite novu lozinku*',
			'required': True,
			'class': "form-control"
			})

		self.fields['current_password'].widget = forms.PasswordInput(attrs={
			'placeholder': 'Unesite trenutnu lozinku*',
			'required': True,
			'class': "form-control"
			})

class AddFriendForm(forms.Form):
	"""
	Forma za dodavanje prijatelja
	"""

	search_field = forms.CharField(widget = forms.EmailInput(attrs={
		'placeholder': 'Unesite email korisnika* ',
		'required': True,
		'class': "form-control"
	}))
