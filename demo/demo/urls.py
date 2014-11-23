from django.conf.urls import patterns, include, url
from demoapp.forms import PasswordResetForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'demoapp.views.home', name='home'),
    url(r'^login', 'demoapp.views.login_user'),
    url(r'^dashboard/$', 'demoapp.views.dashboard'),
    url(r'^profile/$', 'demoapp.views.user_profile'),
    url(r'^logout/$', 'demoapp.views.logout_user'),
    url(r'^registration/confirm-email/(?P<key>[\w.@+-]+)/$', 'verification.views.email_confirmation'),
    url(r'^profile/resend-email/$', 'verification.views.resend_email'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/','template_name': 'registration/password_reset.html', 'password_reset_form':PasswordResetForm},
        name="password_reset"),
    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',{'template_name':'registration/password_reset_done.html'}),
   (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/user/password/done/','template_name':'registration/password_reset_confirm.html'}),
    (r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete', {'template_name':'registration/password_reset_complete.html'}),)
