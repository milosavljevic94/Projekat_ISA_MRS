from django.contrib import admin

# Register your models here.
from .models import Guest

class GuestModelAdmin(admin.ModelAdmin):
	list_display = ['name', 'surname', 'email', 'guest_password', 'ulogovan']
	#list_display_links = ["name"] #samo da mozemo da kliknemo i na ime i da nam otvori kontakt
	list_filter = ['name', 'surname', 'email']

	search_fields = ['name', 'surname', 'email']

	class Meta:
		model = Guest

admin.site.register(Guest, GuestModelAdmin)
