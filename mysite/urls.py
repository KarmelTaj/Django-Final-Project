import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.shortcuts import render
from home.views import CustomLoginView

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', {})

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    #path('api/', include('mainApp.urls')),
    path('tasks/', include('mainApp.urls', namespace='tasks')),
    path('api/', include('api.urls')),
]

# Assign the custom 404 error handler
handler404 = custom_page_not_found_view

# Serve the static HTML
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns += [
    re_path(r'^site/(?P<path>.*)$', serve,
            {'document_root': os.path.join(BASE_DIR, 'site'),
             'show_indexes': True},
            name='site_path'
            ),
]

# Serve the favicon
urlpatterns += [
    path('favicon.ico', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(BASE_DIR, 'home/static'),
    }),
]

# Switch to social login if it is configured - Keep for later
try:
    from . import github_settings
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
                       path(
                           'accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    print('Using', social_login, 'as the login template')
except:
    print('Using registration/login.html as the login template')

# References
# https://docs.djangoproject.com/en/4.2/ref/urls/#include