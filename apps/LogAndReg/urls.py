from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register), 
    url(r'^login$', views.login),
    url(r'^jobs$', views.Dashboard),
    url(r'^Logout$', views.Logout),
    url(r'^logout$', views.Logout),
    url(r'^new$', views.new),
    url(r'^NewJob$', views.NewJob),
    url(r'^jobs/delete/(?P<JobID>\d+)$', views.delete),
    url(r'^jobs/(?P<JobID>\d+)$', views.view),
    url(r'^jobs/edit/(?P<JobID>\d+)$', views.editpage),
    url(r'^jobs/edit/(?P<JobID>\d+)/PostEdit$', views.edit),
    url(r'^jobs/add/(?P<JobID>\d+)$', views.add),
    url(r'^jobs/giveup/(?P<JobID>\d+)$', views.giveup),
    url(r'^jobs/Complete/(?P<JobID>\d+)$', views.Complete),
]