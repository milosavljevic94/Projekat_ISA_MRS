from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

# Create your models here.

def upload_location(instance, filename):
	GuestModel = instance.__class__
	new_id = GuestModel.objects.order_by("id").last().id + 1

	"""
	instance.__class__ vraca model Guest.
    Onda kreiramo queryset sortiranu po "id"-ima svakog objekta,
    Onda uzimamo poslednji objekat u listi pomocu `.last()`
    Koji ce nam vratiti poslednji kreirani objekat, odnosno poslednjeg kreiranog Gosta
    Dodajemo mu 1, da bi dobili isti id kao i gost kog kreiramo.
	"""

	return "%s/%s" %(new_id, filename)

class Guest(models.Model):
	name = models.CharField(blank = False, max_length = 100)
	surname = models.CharField(blank = False, max_length = 100)
	email = models.EmailField(blank = False, max_length = 200, unique = True)
	guest_password = models.CharField(blank = False, max_length = 50)
	repeat_guest_password = models.CharField(blank = False, max_length = 50)
	slug = models.SlugField(unique = True)
	profile_picture = models.ImageField(upload_to = upload_location,
	 									null = True,
										blank = True,
										width_field="width_field",
										height_field="height_field"
										)
	width_field = models.IntegerField(default = 0, null = True)
	height_field = models.IntegerField(default=0, null = True)
	ulogovan = models.BooleanField(default = False)
	#Vezna vise prema vise, jer korisnik moze da ima 0 ili vise prijatelja, a i moze da bude prijatelj 0 ili vise korisnika
	friends_list = models.ManyToManyField("self", symmetrical = False, blank = True)

	def get_absolute_url(self):
		return reverse("gosti:restorani", kwargs={"slug": self.slug})

def create_slug(instance, new_slug = None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Guest.objects.filter(slug = slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_guest_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
    	instance.slug = create_slug(instance)

pre_save.connect(pre_save_guest_receiver, sender = Guest)
