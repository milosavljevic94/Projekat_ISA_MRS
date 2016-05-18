from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Guest
from manager_app.models import Restoran
from .forms import GuestForm, AuthenticationForm, UpdateGuestProfileForm, ChangeGuestPasswordForm, AddFriendForm
from django.core.mail import send_mail, EmailMessage

# Create your views here.
def guest_registration(request):
	form = GuestForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		password1 = request.POST['guest_password']
		password2 = request.POST['repeat_guest_password']
		if Guest.objects.filter(email = request.POST['email']).exists():
			messages.error(request, 'Uneta email adresa je vec registrovana.', extra_tags='email_exists')
		elif len(request.POST['guest_password']) < 6 or len(request.POST['guest_password']) > 50:
			messages.error(request, 'Lozinka mora da sadrzi 6-50 karaktera.', extra_tags='password_length_error')
		elif request.POST['guest_password'] != request.POST['repeat_guest_password']:
			messages.error(request, 'Lozinke nistu iste.', extra_tags='passwords_dont_match_error')
		else:
			instance = form.save(commit = False)
			instance.save()
			# send_mail('Subject here', 'Here is the message.', 'restoran@efood.com', [instance.email], fail_silently=False)
			form = GuestForm()
			messages.success(request, 'Registracija je bila uspesna, molimo vas ulogujte se.')
			# email = EmailMessage('Validacija profila', 'Mail za validaciju profila', to=[instance.email])
			# email.send()

			return redirect('/gost/login/')

	context = {
		"form": form,
	}

	return render(request, 'registrationpage.html', context)

def guest_login(request):
	"""
	Login verification
	"""
	form = AuthenticationForm(request.POST or None)
	if form.is_valid():
		#instance = form.save(commit = False)
		if Guest.objects.filter(email = request.POST['email_address'], guest_password = request.POST['password']).exists():
			guest = Guest.objects.get(email = request.POST['email_address'], guest_password = request.POST['password'])
			print (guest.email)
			Guest.objects.select_for_update().filter(email = request.POST['email_address'], guest_password = request.POST['password']).update(ulogovan = True)
			return HttpResponseRedirect(guest.get_absolute_url())
		else:
			messages.error(request, 'Uneti podaci nisu ispravni, molimo pokusajte ponovo.', extra_tags = 'login_error')
	else:
		form = AuthenticationForm()
	context = {
		"form": form,
	}

	return render(request, 'loginpage.html', context)

def guest_logout(request, slug=None):
	instance = get_object_or_404(Guest, slug=slug)
	if instance.ulogovan == True:
		instance.ulogovan = False
		instance.save()
		return redirect('/gost/login')

	return HttpResponseRedirect('/gost/login/')

#Ova metoda treba da pronadje posatke o trazenom gostu i da ih prosledi stranici koja ce ih prikazivati
def profil_gosta(request, slug=None):
	instance = get_object_or_404(Guest, slug=slug)
	change_password_form = ChangeGuestPasswordForm(request.POST or None)
	form = UpdateGuestProfileForm(request.POST or None, request.FILES or None, instance=instance)
	# print ("ime korisnika je: " + instance.name + " i on je ulogovan: " + str(instance.ulogovan))
	#Ukoliko se unese direktno link za profil gosta onda se proverava dal je gost ulogovan i ukoliko nije prosledjuje se na login stranicu
	if instance.ulogovan == False:
		return redirect('/gost/login')

	context = {
		"guest": instance,
		"form": form,
		"change_password_form": change_password_form
	}

	return render(request, "base_profil_gosta.html", context)

def profil_update(request, slug=None):
	instance = get_object_or_404(Guest, slug=slug)
	form = UpdateGuestProfileForm(request.POST or None, request.FILES or None, instance=instance)

	if form.is_valid():
		if Guest.objects.filter(email = request.POST['email']).exists():
			guest = Guest.objects.get(email = request.POST['email'])
			if guest.name == instance.name and guest.surname == instance.surname and guest.email == instance.email and guest.profile_picture == instance.profile_picture:
				messages.info(request, "Nema izmenjenih podataka.", extra_tags='no_changes_made')
			else:
				instance = form.save(commit = False)
				instance.save()
				messages.success(request, "Vase izmene su sacuvane", extra_tags='profile_updated')
				return HttpResponseRedirect(instance.get_absolute_url())
		else:
			instance = form.save(commit = False)
			instance.save()
			messages.success(request, "Vase izmene su sacuvane", extra_tags='profile_updated')
			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request, 'Uneta email adresa je vec registrovana', extra_tags='email_exists')
	context = {
		"guest": instance,
		"form": form
	}

	return render(request, "base_profil_gosta.html", context)

# def profil_gosta_restorani(request, slug=None):
# 	instance = get_object_or_404(Guest, slug=slug)
# 	#Ukoliko se unese direktno link za profil gosta onda se proverava dal je gost ulogovan i ukoliko nije prosledjuje se na login stranicu
# 	if instance.ulogovan == False:
# 		return redirect('/gost/login')
#
# 	context = {
# 		"guest": instance,
# 		"friends_list": instance.friends_list
# 	}
#
# 	return render(request, "index.html", context)

def profil_gosta_prijatelji(request, slug=None):
	instance = get_object_or_404(Guest, slug=slug)
	#Ukoliko se unese direktno link za profil gosta onda se proverava dal je gost ulogovan i ukoliko nije prosledjuje se na login stranicu
	if instance.ulogovan == False:
		return redirect('/gost/login')

	form = AddFriendForm(request.POST or None)

	vec_je_dodat = False

	if form.is_valid():
		for prijatelj in instance.friends_list.all():
			if prijatelj.email == request.POST['search_field']:
				vec_je_dodat = True
				break

		if Guest.objects.filter(email = request.POST['search_field']).exists() and instance.email != request.POST['search_field'] and vec_je_dodat == False:
			instance.friends_list.add(Guest.objects.get(email = request.POST['search_field']))
			messages.success(request, "Prijatelj je uspesno dodat.", extra_tags='friend_added')
		elif instance.email == request.POST['search_field']:
			messages.error(request, 'Uneta email adresa pripada vama. ', extra_tags='entered_self_email')
		elif vec_je_dodat == True:
			messages.error(request, 'Prijatelj je vec dodat. ', extra_tags='friend_already_added')
		else:
			messages.error(request, 'Korisnik sa unetom email adresom ne postoji', extra_tags='wrong_email_address')

	context = {
		"search_friend_form": form,
		"guest": instance,
		"friends_list": instance.friends_list.all
	}

	return render(request, "profil_gosta_prijatelji.html", context)

def change_guest_password(request, slug = None):

	instance = get_object_or_404(Guest, slug=slug)

	#Ukoliko se unese direktno link za profil gosta onda se proverava dal je gost ulogovan i ukoliko nije prosledjuje se na login stranicu
	if instance.ulogovan == False:
		return redirect('/gost/login')

	form = ChangeGuestPasswordForm(request.POST or None)

	if form.is_valid():
		if instance.guest_password == request.POST['current_password']:
			print ("Usao je ovde")
			guest = Guest.objects.get(email = instance.email, guest_password = request.POST['current_password'])
			print ("Nesto se ispisalo " + guest.guest_password)
			if len(request.POST['guest_password']) < 6 or len(request.POST['guest_password']) > 50:
				messages.error(request, 'Lozinka mora da sadrzi 6-50 karaktera.', extra_tags='changed_password_length_error')
			elif request.POST['guest_password'] != request.POST['repeat_guest_password']:
				messages.error(request, 'Lozinke nistu iste.', extra_tags='changed_passwords_dont_match_error')
			else:
				Guest.objects.select_for_update().filter(email = instance.email, guest_password = request.POST['current_password']).update(guest_password = request.POST['guest_password'], repeat_guest_password = request.POST['repeat_guest_password'])
				messages.success(request, "Lozinka je uspesno izmenjena", extra_tags='password_changed')
				return HttpResponseRedirect(guest.get_absolute_url())
		else:
			messages.error(request, "Pogresna lozinka", extra_tags='wrong_current_password')

	context = {
		"change_password_form": form
	}

	return render(request, "base_profil_gosta.html", context)

def lista_restorana(request, slug=None):
	queryset_list = Restoran.objects.all() #.order_by("-timestamp")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(naziv__icontains=query)
				#Q(content__icontains=query)|
				#Q(user__first_name__icontains=query) |
				#Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset,
		"page_request_var": page_request_var,
	}
	return render(request, "index.html", context)
