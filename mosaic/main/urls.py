from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('mosaic.main.views',
    # Examples:
    # url(r'^$', 'mosaic.views.home', name='home'),
    url(r'^$', 'home', name='home'),
    url(r'^request/(?P<rid>\d+)/$', 'req', name='req'),
    url(r'^request/new/$', 'new', name='new'),
    url(r'^request/$', 'req', name='req'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
