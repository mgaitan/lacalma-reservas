from django.conf.urls import include, url
from django.contrib import admin
from lacalma.views import (
    reserva_view, gracias, gracias_mp, presupuesto, mp_notification, regenerar_mercadopago,
    temporadas_vigentes
)

urlpatterns = [
    # Examples:
    # url(r'^$', 'reservas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/lacalma/reserva/(?P<id>\d+)/regenerar-mercadopago',
        regenerar_mercadopago, name='regenerar_mercadopago'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gracias/$', gracias, name='gracias'),
    url(r'^gracias/success$', gracias_mp, name='gracias_mp'),
    url(r'^presupuesto/(?P<id>\d+)$', presupuesto, name="presupuesto"),
    url(r'^ipn$', mp_notification, name='ipn'),
    url(r'^encuesta/', include('encuesta.urls')),
    url(r'^retiros/', include('retiros.urls')),
    url(r'^export_action/', include("export_action.urls", namespace="export_action")),
    url(r'^temporadas-vigentes/$', temporadas_vigentes, name='temporadas_vigentes'),
    url(r'^$', reserva_view)
]