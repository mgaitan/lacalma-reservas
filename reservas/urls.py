from django.conf.urls import patterns, include, url
from django.contrib import admin
from lacalma.views import reserva_view, gracias, gracias_mp, detalle, mp_notification

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reservas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^gracias/$', gracias, name='gracias'),
    url(r'^gracias/success$', gracias_mp, name='gracias_mp'),
    url(r'^detalle/(?P<id>\d+)$', detalle),
    url(r'^mp-notificacion$', mp_notification),
    url(r'^$', reserva_view)

)
