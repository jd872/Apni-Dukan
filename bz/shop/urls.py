from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="ShopHome"),
    path('about/', views.about,name="AboutUs"),
    path('contact/', views.contact,name="ContactUs"),
    path('tracker/', views.tracker,name="TrackingStatus"),
    path('search/', views.search,name="Search"),
    path('login/', views.login,name="Login"),
    path('logout/', views.logout,name="Logout"),
    path('register/', views.Register,name="Register"),
    path('products/<int:myid>', views.productview,name="product"),
    path('checkout/', views.checkout,name="checkout"),


]
