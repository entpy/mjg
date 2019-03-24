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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from mjg_site.consts import project_constants
import website.views

handler404 = 'website.views.www_404'
handler500 = 'website.views.www_500'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', website.views.www_index, name='www_index'),
    url(r'^index/$', website.views.www_index, name='www_index'),
    url(r'^servizi/?$', website.views.www_services, name='www_services'),
    url(r'^contattaci/?$', website.views.www_contacts, name='www_contacts'),
    # TODO: testare che con i parametri al fondo master_code continui a funzionare
    url(r'^ricevi-offerte/(?:(?P<master_code>[^\/]+)/)?$', website.views.www_get_offers, {'source': project_constants.SOURCE_GET_OFFERS}),
    url(r'^meccatronica/?$', website.views.www_mechanics, name='www_mechanics'),
    url(r'^gommista/?$', website.views.www_tires, name='www_tires'),
    url(r'^tagliando-completo/?$', website.views.www_checkup, name='www_checkup'),
    url(r'^privacy/?$', website.views.www_privacy_cookie_policy, name='www_privacy_cookie_policy'),
    url(r'^cookie-policy/?$', website.views.www_cookie_law, name='www_cookie_law'),
    url(r'^disiscriviti/(?P<user_id>\d+)/(?P<account_code>[^\/]+)/(?:(?P<unsubscribe_type>\w+)/)?$', website.views.www_unsubscribe, name='www_unsubscribe'),
    url(r'^profilo/(?P<user_id>\d+)/(?P<account_code>[^\/]+)/(?:(?P<show_only_section>\w+)/)?$', website.views.www_profile, name='www_profile'),
    url(r'^feedback/(?P<user_id>\d+)/(?P<account_code>[^\/]+)/?$', website.views.www_feedback, name='www_feedback'),
    url(r'^invita-amici/(?P<user_id>\d+)/(?P<account_code>[^\/]+)/?$', website.views.www_refer_friends, name='www_refer_friends'),
    url(r'^lascia-una-recensione/(?P<user_id>\d+)/(?P<account_code>[^\/]+)/?$', website.views.www_get_review, name='www_get_review'),

    # flyer 30
    url(r'^volantino/?$', website.views.www_get_offers, {'source': project_constants.SOURCE_FLYER_30}),
    # flyer checkup
    url(r'^offerta/?$', website.views.www_get_offers, {'source': project_constants.SOURCE_FLYER_CHECKUP}),

    # dashboard {{{
    url(r'^dashboard/?$', website.views.dashboard_index, name='dashboard_index'),
    url(r'^dashboard/customers/?$', website.views.dashboard_customers, name='dashboard_customers'),
    url(r'^dashboard/validate-coupon/?$', website.views.dashboard_validate_coupon, name='dashboard_validate_coupon'),
    url(r'^dashboard/set-customer/(?:(?P<user_id>\d+)/)?$', website.views.dashboard_set_customer, name='dashboard_set_customer'),
    # fare pagina nascosta per inviare il bonus della recensione (attivabile tramite pulsante nella mail)
    url(r'^dashboard/review-prize/(?P<user_id>\d+)/(?P<account_code>[^\/]+)/?$', website.views.dashboard_review_prize, name='dashboard_review_prize'),
    # pagina raggiungibile solo da URL per inizializzare la mkauto
    url(r'^dashboard/create-mkauto-default/?$', website.views.dashboard_create_mkauto_default, name='dashboard_create_mkauto_default'),
    # campagne
    url(r'^dashboard/campaigns/?$', website.views.dashboard_campaigns_index, name='dashboard_campaigns_index'),
    url(r'^dashboard/campaigns/step1/?$', website.views.dashboard_campaigns_step1, name='dashboard_campaigns_step1'),
    url(r'^dashboard/campaigns/step2/?$', website.views.dashboard_campaigns_step2, name='dashboard_campaigns_step2'),
    url(r'^dashboard/campaigns/step3/?$', website.views.dashboard_campaigns_step3, name='dashboard_campaigns_step3'),
    url(r'^dashboard/campaigns/stats/?$', website.views.dashboard_campaigns_stats, name='dashboard_campaigns_stats'),
    # dashboard }}}

    # ajax {{{
    url(r'^ajax/customers-list/?$', website.views.ajax_customers_list, name='ajax_customers_list'),
    url(r'^ajax/ajax-upload-campaign-image/?$', website.views.ajax_upload_campaign_image, name='ajax_upload_campaign_image'),
    # ajax }}}

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
