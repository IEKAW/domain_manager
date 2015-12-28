from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^server$', views.server),
    url(r'^domain$', views.domain),
    url(r'^site$', views.site),
    url(r'^domain/unupdate$', views.domain_unup),
    url(r'^server/unupdate$', views.server_unup),
]
