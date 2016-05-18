from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from .views import (
	guest_registration,
    guest_login,
	profil_gosta,
	lista_restorana,
	profil_gosta_prijatelji,
	guest_logout,
	profil_update,
	change_guest_password,
	profil_gosta_prijatelji,
	)

urlpatterns = [
	url(r'^registration/$', guest_registration),
    url(r'^login/$', guest_login),
    url(r'^(?P<slug>[\w-]+)/profil/$', profil_gosta),
	url(r'^(?P<slug>[\w-]+)/restorani/$', lista_restorana, name='restorani'),
	#url(r'^', guest_login),
	url(r'^(?P<slug>[\w-]+)/prijatelji/$', profil_gosta_prijatelji),
	url(r'^(?P<slug>[\w-]+)/logedout/$', guest_logout),
	url(r'^(?P<slug>[\w-]+)/update/$', profil_update),
	url(r'^(?P<slug>[\w-]+)/changepassword/$', change_guest_password),
	url(r'^(?P<slug>[\w-]+)/searchfriend/$', profil_gosta_prijatelji),
    #url(r'^home/$', guest_registration),
]
