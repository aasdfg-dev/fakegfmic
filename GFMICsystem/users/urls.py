from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'users'
 
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('error_404/', views.error_404, name='error_404'),
    path('forgot-pw/', views.forgot_pass, name="forgot_pass"),
    path('register/', views.register, name='register'),
    path('register_account/', views.register_account, name='register_account'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/', views.process_login, name='process_login'),
    path('about/', views.about, name='about'),
    path('gfmic-event/', views.home_event, name='home_event'),
    path('webinar/', views.webinar, name='webinar'),
    path('membership-conference/', views.membership_conference, name='membership_conference'),
    path('national-convention/', views.national_convention, name='national_convention'),
    path('faqs/', views.faqs, name='faqs'),
    path('help-desk/', views.help_desk, name='help_desk'),

    path('payment', views.payment, name='payment'),
    path('membership/', views.membership, name='membership'),
    path('add_profile/', views.profile, name='profile'),
    path('ecert/', views.ecert, name='ecert'),
    path('generator/', views.generator, name='generator'),

    path('add_membership/', views.add_membership, name='add_membership'),
    path('view_membership/', views.view_membership, name='view_membership'),
    path('approve_membership/', views.approve_membership, name='approve_membership'),
    path('disapprove_membership/', views.disapprove_membership, name='disapprove_membership'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),

    path('events/', views.events, name='events'),
    path('event/', views.event, name='event'),
    path('add_event/', views.add_event, name='add_event'),
    path('event', views.add_event_picture, name='add_event_picture'),
    path('view_event/', views.view_event, name='view_event'),
    path('event_remove/', views.event_remove, name='event_remove'),
    path('event_approve/', views.event_approve, name='event_approve'),
    path('join_event_payment/', views.event_approve, name='join_event_payment'),

    path('or/', views.OR, name='OR'),
    path('member_gen_receipt/', views.member_gen_receipt, name='member_gen_receipt'),

    path('add_ecert/', views.member_gen_receipt, name='add_ecert'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)