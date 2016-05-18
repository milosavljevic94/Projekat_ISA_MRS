from django.shortcuts import render
from .forms import RestoranForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Restoran


# Create your views here.
def azuriranje_profila_restorana(request, slug=None):
	instance = get_object_or_404(Restoran, slug=slug)
	form = RestoranForm(request.POST or None,instance=instance)

	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Vase izmene su sacuvane", extra_tags='profile_updated')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"restoran": instance,
		"lista_slika": instance.slike.slika.all,
		"form": form
	}

	return render(request, "profil_restorana.html", context)
