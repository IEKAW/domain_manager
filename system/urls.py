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
    url(r'^link/(?P<site_id>\d+)$', views.link, name='link'),
    url(r'^domain/create$', views.create_domain),
    url(r'^server/create$', views.create_server),
    url(r'^link/create$', views.create_link),
    # url(r'link.json$', views.link_json),
    url(r'^site/create$', views.create_site),
    url(r'^setting$', views.setting),
    url(r'^setting/templates$', views.setting_templates),
    url(r'^setting/link$', views.setting_link),
    url(r'^setting/group$', views.setting_group),
    url(r'^setting/payment$', views.setting_payment),
    url(r'^setting/domain$', views.setting_domain),
    url(r'^setting/server$', views.setting_server),
    url(r'^setting/group/create$', views.create_setting_group),
    url(r'^setting/server/create$', views.create_setting_server),
    url(r'^setting/domain/create$', views.create_setting_domain),
    url(r'^setting/payment/create$', views.create_setting_payment),
    url(r'^setting/templates/create$', views.create_setting_templates),
    url(r'^setting/link/create$', views.create_setting_link),
    url(r'^delete$', views.delete),
    url(r'^delete_all$', views.delete_all),
    url(r'^warning$', views.domain_warning),
    url(r'^comment/edit$', views.comment_edit),
    url(r'^comment/delete$', views.comment_delete),
    url(r'^comment/all$', views.comment_all),
    url(r'^url_site.json$', views.url_to_site),
    url(r'^setting/group/edit$', views.group_edit),
    url(r'^setting/templates/edit$', views.templates_edit),
    url(r'^setting/link/edit$', views.setting_link_edit),
    url(r'^setting/payment/edit$', views.payment_edit),
    url(r'^setting/domain/edit$', views.domain_edit),
    url(r'^setting/server/edit$', views.setting_server_edit),
    url(r'^keyword$', views.rank),
    url(r'^keyword/create$', views.create_keyword),
    url(r'^updomain$', views.updomain),
    url(r'^upserver$', views.upserver),
]
