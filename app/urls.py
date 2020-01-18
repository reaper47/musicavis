from django.urls import path, include
from django.contrib.auth import views as auth_views

from app.backend.contact.views import contact_us
from app.backend.auth.forms import LoginForm
from app.backend.auth.views import login_view, signup_view
from app.backend.main.views import (index_view, sitemap_view, notifications_route, download_file_route,
                                    pricing_view, features_view)
from app.backend.legal.views import privacy_view, terms_view


app_name = 'app'
urlpatterns = [
    path('', index_view, name='main.index'),
    #path('', include('django.contrib.auth.urls')),

    path('export/<fname>/', download_file_route, name='main.export'),
    path('features/', features_view, name='main.features'),
    path('notifications/', notifications_route, name='main.notifications'),
    path('pricing/', pricing_view, name='main.pricing'),
    path('sitemap/', sitemap_view, name='main.sitemap'),

    path('contact-us/', contact_us, name='contact.contact_us'),

    path('privacy/', privacy_view, name='legal.privacy'),
    path('terms/', terms_view, name='legal.terms'),

    path('login/', login_view, name='auth.login'),
    path('logout/', auth_views.LogoutView.as_view(), name='auth.logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='auth.password_reset'),
    path('signup/', signup_view, name='auth.signup'),

    path('dashboard/', contact_us, name='dashboard.index'),

    path('profile/', contact_us, name='profile.profile'),

    path('practice/', contact_us, name='practice.new'),
    path('practice/list/', contact_us, name='practice.list_past_practices')
]
