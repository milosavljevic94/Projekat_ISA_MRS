from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from .views import (
	azuriranje_profila_restorana,
	)

urlpatterns = [
	url(r'^(?P<slug>[\w-]+)/$', azuriranje_profila_restorana, name='restoran'),
    #url(r'^home/$', guest_registration),
]
