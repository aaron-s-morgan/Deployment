from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('user/create_user', views.create_user),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('dashboard', views.dashboard),
    path('trips/new', views.create),
    path('trips/submit', views.create_trip),
    path('trips/<int:trip_id>', views.show_trip),
    path('trips/edit/<int:trip_id>', views.edit),
    path('trips/submit/<int:trip_id>', views.edit_trip),
    path('trips/delete/<int:trip_id>', views.delete_trip),
    path("join/<int:trip_id>", views.join),
    path("unjoin/<int:trip_id>", views.unjoin),
]
