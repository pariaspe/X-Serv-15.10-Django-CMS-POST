from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.contrib.auth.views import login

urlpatterns = [
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout', logout),
    url(r'^login', login),
    url(r'^annotated/$', 'cms_post.views.annotated_barra'),
    url(r'^annotated/(.*)$', 'cms_post.views.annotated_other'),
    url(r'^edit/(.*)$', 'cms_post.views.edit'),
    url(r'^$', 'cms_post.views.barra'),
    url(r'^(.*)$', 'cms_post.views.other'),
]
