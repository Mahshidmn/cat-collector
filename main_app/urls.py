from django.urls import path
from . import views

# Prefer convention over configuration
urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('cats/', views.cats_index, name="index"),
    path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),
    path('cats/create/', views.CatCreate.as_view(), name='cats_create'),
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cats_update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cats_delete'),
    path('cats/<int:cat_id>/add_toy/<int:toy_id>/', views.add_toy, name='add_toy'), 
    path('cats/<int:cat_id>/remove_toy/<int:toy_id>/', views.remove_toy, name='remove_toy'), 

    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),

    path('accounts/signup/', views.signup, name='signup'),
]

