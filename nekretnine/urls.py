from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('zaboravljena-lozinka/', views.zaboravljena_lozinka, name='zaboravljena_lozinka'),

    # prodaja
    path('prodaja-stanova/', views.prodaja_stanova, name='prodaja_stanova'),

    # agencije
    path('agencije/', views.agencije, name='agencije'),

    # investitoti
    path('investitor/', views.investitor, name='investitor'),

    # korisnik
    path('sacuvane-pretrage/', views.sacuvane_pretrage, name='sacuvane_pretrage'),
    path('sacuvani-oglasi/', views.sacuvani_oglasi, name='sacuvani_oglasi'),
    path('postavi-oglas/', views.postavi_oglas, name='postavi_oglas'),
    path('moji-oglasi/', views.moji_oglasi, name='moji_oglasi'),
    path('podesavanja/', views.podesavanja, name='podesavanja'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)