from django.urls import path

from . import views
from .forms import LoginForm

from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('',views.home_view,name='home'),
    path('users/',views.users_list,name='users_list'),
    path('user/<slug:slug>',views.user_detail,name='user_detail'),
    path('user/update/<slug:slug>',views.user_update,name='user_update'),
    path('user/delete/<slug:slug>',views.user_delete,name='user_delete'),
    path('user/create/',views.user_create,name='user_create'),
    path('login/',LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('restaurant/',views.restaurant_list,name='restaurant_list'),
    path('restaurant/<slug:slug>',views.restaurant_detail,name='restaurant_detail'),
    path('restaurant/create/',views.restaurant_create,name='restaurant_create'),
    path('restaurant/update/<slug:slug>',views.restaurant_update,name='restaurant_update'),
    path('restaurant/delete/<slug:slug>',views.restaurant_delete,name='restaurant_delete'),
    path('dish/create/<slug:slug>',views.dish_create,name='dish_create'),
    path('dish/update/<slug:slug>',views.dish_update,name='dish_update'),
    path('dish/delete/<slug:slug>',views.dish_delete,name='dish_delete'),
]
