from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^signup/$', views.signup, name='signup'),
    url('^login/$', views.login, name='login'),
    url('^logout/$', views.logout, name='logout'),
    url('^recruit/$', views.recruit, name='recruit'),
    url('^recruit/(?P<page>[^/]+)/$', views.recruit, name='recruit'),
    url('^tickets/$', views.tickets, name='tickets'),
    url('^ticket/(?P<ticket_id>[^/]+)/$', views.assign, name='assign'),
    url('^review/(?P<ticket_id>[^/]+)/$', views.review, name='review'),
    url('^thankyou/(?P<msg_code>[0-9]+)/$', views.thankyou, name='thankyou'),
    url('^fire/$', views.fire, name='fire'),
    url('^tryrecruit/$', views.tryRecruit, name='tryrecruit'),
    url('^toggleavailability/$', views.toggleAvailability, name='toggleavailability'),
    url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/edit/$', views.profileEdit, name='profileEdit')
]