"""mjg_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import website.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', website.views.www_index, name='www_index'),
    url(r'^index/$', website.views.www_index, name='www_index'),
    url(r'^servizi/?$', website.views.www_services, name='www_services'),
    url(r'^contattaci/?$', website.views.www_contacts, name='www_contacts'),
    url(r'^prenota-servizio/?$', website.views.www_service_booking, name='www_service_booking'),
    url(r'^ricevi-offerte/?$', website.views.www_get_offers, name='www_get_offers'),
    url(r'^meccatronica/?$', website.views.www_mechanics, name='www_mechanics'),
    url(r'^gommista/?$', website.views.www_tires, name='www_tires'),
    url(r'^tagliando-completo/?$', website.views.www_checkup, name='www_checkup'),
    url(r'^privacy/?$', website.views.www_privacy_cookie_policy, name='www_privacy_cookie_policy'),
    url(r'^cookie-policy/?$', website.views.www_cookie_law, name='www_cookie_law'),
    url(r'^disiscriviti/(?P<user_id>\d+)/(?P<account_code>[^\/]+)/(?P<unsubscribe_type>\w+)/$', website.views.www_unsubscribe, name='www_unsubscribe'),

    url(r'^test-page/?$', website.views.www_test_page, name='www_test_page'),
]
