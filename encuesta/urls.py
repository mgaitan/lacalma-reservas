from django.conf.urls import patterns, include, url
from encuesta.views import encuesta, gracias, completa

urlpatterns = patterns('',
        url(r'^gracias/$', gracias, name='encuesta_gracias'),

        url(r'^completa/$', completa, name='encuesta_completa'),

        url(r'^(?P<uuid>[a-z0-9]+)/$', encuesta, name='encuesta'),

)