from django.urls import path
from django.contrib.auth import views as auth_views

from app.backend.contact.views import contact_us
from app.backend.auth.views import (login_view, signup_view, account_confirm, resend_account_confirm, logout_view,
                                    password_reset_view, request_password_reset_view, unsubscribe_view)
from app.backend.main.views import (index_view, sitemap_view, notifications_route, download_file_route,
                                    pricing_view, features_view)
from app.backend.legal.views import privacy_view, terms_view


app_name = 'app'
urlpatterns = [
    path('', index_view, name='main.index'),

    path('export/<fname>/', download_file_route, name='main.export'),
    path('features/', features_view, name='main.features'),
    path('notifications/', notifications_route, name='main.notifications'),
    path('pricing/', pricing_view, name='main.pricing'),
    path('sitemap/', sitemap_view, name='main.sitemap'),

    path('contact-us/', contact_us, name='contact.contact_us'),
    path('privacy/', privacy_view, name='legal.privacy'),
    path('terms/', terms_view, name='legal.terms'),

    path('login/', login_view, name='auth.login'),
    path('logout/', logout_view, name='auth.logout'),
    path('signup/', signup_view, name='auth.signup'),
    path('confirm/<token>/', account_confirm, name='auth.confirm'),
    path('confirm-new/<token>/', resend_account_confirm, name='auth.resend_confirm'),
    path('request_password_reset/', request_password_reset_view, name='auth.request_password_reset'),
    path('password_reset/<token>/', password_reset_view, name='auth.password_reset'),
    path('unsubscribe/<token>/', unsubscribe_view, name='auth.unsubscribe'),

    path('dashboard/', contact_us, name='dashboard.index'),
    path('profile/', contact_us, name='profile.profile'),
    path('profile/settings', contact_us, name='profile.settings'),

    path('practice/', contact_us, name='practice.new'),
    path('practice/list/', contact_us, name='practice.list_past_practices')
]
