from django.urls import path

from app.backend.contact.views import contact_us
from app.backend.auth.views import (login_view, signup_view, account_confirm, resend_account_confirm, logout_view,
                                    password_reset_view, request_password_reset_view, unsubscribe_view)
from app.backend.main.views import (index_view, sitemap_view, notifications_route, download_file_route,
                                    pricing_view, features_view)
from app.backend.legal.views import privacy_view, terms_view
from app.backend.profile.views import (profile_view, export_practices_view, settings_view, settings_access_view,
                                       settings_profile_view, settings_practice_view, add_new_instrument_view,
                                       delete_account_view)
from app.backend.practice.views import new_view, session_view, list_past_practices_view
from app.backend.dashboard.views import dashboard_index_view


app_name = 'app'
urlpatterns = [
    path('', index_view, name='main.index'),

    path('exports/<fname>/', download_file_route, name='main.export'),
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

    path('dashboard/', dashboard_index_view, name='dashboard.index'),

    path('profile/', profile_view, name='profile.profile'),
    path('settings/', settings_view, name='profile.settings'),
    path('settings/access/', settings_access_view, name='profile.settings_access'),
    path('settings/practice', settings_practice_view, name='profile.settings_practice'),
    path('settings/profile', settings_profile_view, name='profile.settings_profile'),
    path('add-new-instrument/', add_new_instrument_view, name='profile.add_new_instrument'),
    path('delete-account/', delete_account_view, name='profile.delete_account'),
    path('export-practices/', export_practices_view, name='profile.export_practices'),

    path('practice/', new_view, name='practice.new'),
    path('practice/<int:practice_id>', session_view, name='practice.session'),
    path('practice/list/', list_past_practices_view, name='practice.list_past_practices')
]
