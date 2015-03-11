from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import inscripcion, gracias, gracias_mp, mp_notification, normas


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reservas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<retiro_id>\d+)/$', inscripcion, name="retiros_inscripcion"),
    url(r'^normas$', normas, name='normas'),
    url(r'^gracias/$', gracias, name='retiros_gracias'),
    url(r'^gracias/success$', gracias_mp, name='retiros_gracias_mp'),
    url(r'^ipn$', mp_notification, name='retiros_ipn'),

)
