from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.profile, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/cv/', views.cv, name='cv'),
    path('profile/cv/<int:pk>/', views.cv_pk, name='cv_pk'),
    path('profile/cv/<int:pk>/edit/', views.cv_edit, name='cv_edit'),
    path('logout/', views.logout, name='logout'),
]
