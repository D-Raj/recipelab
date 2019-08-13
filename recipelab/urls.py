from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recipelab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^analyze/', include('analyze.urls')),
    url(r'^fastspring/', include('django_fastspring.urls')),

    url(r'^$', TemplateView.as_view(template_name="home.html")),
    url(r'^userguide/', TemplateView.as_view(template_name="userguide.html"), name='userguide'),
    url(r'^profile/', TemplateView.as_view(template_name="profile.html"), name='profile'),
    url(r'^terms/', TemplateView.as_view(template_name="terms.html"), name='terms'),
    url(r'^privacy/', TemplateView.as_view(template_name="privacy.html"), name='privacy'),
    url(r'^pricing/', TemplateView.as_view(template_name="pricing.html"), name='pricing'),
    url(r'^support/', TemplateView.as_view(template_name="support.html"), name='support'),

#   django-registration handling all account-related views - simple version does NOT require email confirmation
    url(r'^accounts/', include('registration.backends.simple.urls')),
#    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
