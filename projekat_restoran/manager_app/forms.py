from .models import Restoran
from django import forms
from django.contrib import messages

class RestoranForm(forms.ModelForm):
	"""
	Registration form
	"""
	class Meta:
		model = Restoran
		fields = [
			'naziv', 'grad','ulica', 'opis', 'tip',
		]

	#pomocu ovog dole moguce je primenjivati razlicite nacine za styling nasih polja odradjenih preko djanga
	def __init__(self, *args, **kwargs):
		super(RestoranForm, self).__init__(*args, **kwargs)
		self.fields['naziv'].widget = forms.TextInput(attrs={
			'placeholder': 'Naziv*',
			'required': True,
			'class': "form-first-name form-control"
			})

		self.fields['grad'].widget = forms.TextInput(attrs={
			'placeholder': 'grad*',
			'required': True,
			'class': "form-first-name form-control"
			})

		self.fields['ulica'].widget = forms.TextInput(attrs={
			'placeholder': 'ulica*',
			'required': True,
			'class': "form-first-name form-control"
			})

		self.fields['opis'].widget = forms.TextInput(attrs={
			'placeholder': 'opis*',
			'required': True,
			'class': "form-first-name form-control"
			})

		self.fields['tip'].widget = forms.TextInput(attrs={
			'placeholder': 'tip*',
			'required': True,
			'class': "form-first-name form-control"
			})
