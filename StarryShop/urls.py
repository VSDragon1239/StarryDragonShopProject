# StarryShop/urls.py
from django.urls import path
from .views import IndexView, MyTemplateView, AuthLoginView, AuthReginView, UserCartView, ItemSearchView, \
    UserProfileView, UserOutlogView, ItemDetailsView

urlpatterns = [
    path('', IndexView.as_view(), name='main'),               # Главная страница
    path('catalog/<int:pk>/products/<int:pk2>', ItemDetailsView.as_view(), name='product'),               # Главная страница
    path('catalog/0/search/', ItemSearchView.as_view(), name='search'),               # Главная страница
    path('auth/login/', AuthLoginView.as_view(), name='login'),               # Главная страница
    path('auth/reg/', AuthReginView.as_view(), name='reg'),               # Главная страница
    path('user/cart/', UserCartView.as_view(), name='user_cart'),               # Главная страница
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),               # Главная страница
    path('user/outlog/', UserOutlogView.as_view(), name='user_outlog'),               # Главная страница
    path('test/', MyTemplateView.as_view(), name='test'),       # Страница "О проекте"
]
