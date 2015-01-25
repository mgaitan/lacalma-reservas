from django.conf.urls import patterns, include, url
from django.contrib import admin
from lacalma.views import reserva_view, gracias, gracias_mp, presupuesto, mp_notification

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reservas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^gracias/$', gracias, name='gracias'),
    url(r'^gracias/success$', gracias_mp, name='gracias_mp'),
    url(r'^presupuesto/(?P<id>\d+)$', presupuesto, name="presupuesto"),
    url(r'^ipn$', mp_notification, name='ipn'),
    url(r'^$', reserva_view)

)
