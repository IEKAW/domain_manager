from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^server$', views.server),
    url(r'^domain$', views.domain),
    url(r'^site$', views.site),
    url(r'^domain/unupdate$', views.domain_unup),
    url(r'^server/unupdate$', views.server_unup),
    url(r'^domain/detail$', views.domain_detail),
    url(r'^server/detail$', views.server_detail),
    url(r'^domain/update$', views.update_domain),
    url(r'^server/update$', views.update_server),
    url(r'^site/detail$', views.site_detail),
    url(r'^link$', views.link),
    url(r'^domain/create$', views.create_domain),
    url(r'^server/create$', views.create_server),
    url(r'^link/create$', views.create_link),
    url(r'^site/create$', views.create_site),
    url(r'^setting$', views.setting),
    url(r'^delete$', views.delete),
    url(r'^delete_all$', views.delete_all),
    url(r'^warning$', views.domain_warning),
    url(r'^comment/edit$', views.comment_edit),
    url(r'^comment/delete$', views.comment_delete),
    url(r'^comment/all$', views.comment_all)
]
