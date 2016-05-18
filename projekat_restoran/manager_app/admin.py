from django.contrib import admin

from .models import Menadzer,Restoran,TipoviRestorana,GalerijaSlikaRestorana,slika

# Register your models here.
class MenadzerModelAdmin(admin.ModelAdmin):
	list_display = ['ime', 'prezime', 'email']
	#list_display_links = ["name"] #samo da mozemo da kliknemo i na ime i da nam otvori kontakt
	list_filter = ['ime', 'prezime', 'email']

	search_fields = ['ime', 'prezime', 'email']

	class Meta:
		model = Menadzer

class TipoviRestoranaModelAdmin(admin.ModelAdmin):
	list_display = ['nazivTipa']
	#list_display_links = ["name"] #samo da mozemo da kliknemo i na ime i da nam otvori kontakt
	list_filter = ['nazivTipa']

	search_fields = ['nazivTipa']

	class Meta:
		model = TipoviRestorana

class GalerijaSlikaRestoranaModelAdmin(admin.ModelAdmin):
	list_display = ['naziv']
	#list_display_links = ["name"] #samo da mozemo da kliknemo i na ime i da nam otvori kontakt

	class Meta:
		model = GalerijaSlikaRestorana


class RestoranModelAdmin(admin.ModelAdmin):
	list_display = ['naziv','menadzer']
	#list_display_links = ["name"] #samo da mozemo da kliknemo i na ime i da nam otvori kontakt
	list_filter = ['naziv']

	search_fields = ['naziv']

	class Meta:
		model = Restoran

admin.site.register(Menadzer, MenadzerModelAdmin)
admin.site.register(Restoran, RestoranModelAdmin)
admin.site.register(TipoviRestorana, TipoviRestoranaModelAdmin)
admin.site.register(GalerijaSlikaRestorana, GalerijaSlikaRestoranaModelAdmin)
admin.site.register(slika)