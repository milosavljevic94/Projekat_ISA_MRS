from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

class Menadzer(models.Model):
	ime = models.CharField(blank = False, max_length = 100)
	prezime = models.CharField(blank = False, max_length = 100)
	email = models.EmailField(blank = False, max_length = 200, unique = True)
	slug = models.SlugField(unique = True)


	def get_absolute_url(self):
		return reverse("menadzer:restorani", kwargs={"slug": self.slug})

	def __unicode__(self):
		return self.ime + " " + self.prezime


def create_slug_menadzer(instance, new_slug = None):
	slug = slugify(instance.ime)
	if new_slug is not None:
		slug = new_slug
	qs = Menadzer.objects.filter(slug = slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
    	instance.slug = create_slug(instance)


def upload_location(instance, filename):
	GalerijaModel = instance.__class__

	"""
	instance.__class__ vraca model Guest.
    Onda kreiramo queryset sortiranu po "id"-ima svakog objekta,
    Onda uzimamo poslednji objekat u listi pomocu `.last()`
    Koji ce nam vratiti poslednji kreirani objekat, odnosno poslednjeg kreiranog Gosta
    Dodajemo mu 1, da bi dobili isti id kao i gost kog kreiramo.
	"""

	return "%s" %(filename)

class slika(models.Model):
	s = models.ImageField(upload_to = upload_location,
	 									null = True,
										blank = True,
										width_field="width_field",
										height_field="height_field"
										)
	width_field = models.IntegerField(default = 0, null = True)
	height_field = models.IntegerField(default=0, null = True)

	def __unicode__(self):
		return self.s.url

#Slike restorana, bice vise slika.
class GalerijaSlikaRestorana(models.Model):
	naziv = models.CharField(blank = False, max_length = 100)
	slika = models.ManyToManyField(slika, symmetrical = False, blank = True)
	
	def __unicode__(self):
		return self.naziv


class TipoviRestorana(models.Model):
	nazivTipa = models.CharField(blank = False, max_length = 100)

	def __unicode__(self):
		return self.nazivTipa


class Restoran(models.Model):
	"""Klasa Restoran"""
	naziv = models.CharField(blank = False, max_length = 100)
	ulica = models.CharField(blank = False, max_length = 100)
	grad = models.CharField(blank = False, max_length = 100)
	slug = models.SlugField(unique = True)
	menadzer = models.ForeignKey(Menadzer, on_delete=models.CASCADE)
	slike = models.ForeignKey(GalerijaSlikaRestorana, on_delete=models.CASCADE)
	tip = models.ForeignKey(TipoviRestorana, on_delete=models.CASCADE)
	opis = models.CharField(blank = False, max_length = 1000)

	def get_absolute_url(self):
		return reverse("restoran:restoran", kwargs={"slug": self.slug})

def create_slug_restoran(instance, new_slug = None):
	slug = slugify(instance.naziv)
	if new_slug is not None:
		slug = new_slug
	qs = Restoran.objects.filter(slug = slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

pre_save.connect(pre_save_receiver, sender = Restoran)
pre_save.connect(pre_save_receiver, sender = Menadzer)