# StarryShop/urls.py
from django.urls import path
from .views import IndexView, MyTemplateView, AuthLoginView, AuthReginView, UserCartView, ItemSearchView, \
    UserProfileView, UserOutlogView, ItemDetailsView, AddToCartView, UpdateCartItemView, RemoveFromCartView, \
    MergeGuestCartView

urlpatterns = [
    path('', IndexView.as_view(), name='main'),               # Главная страница
    path('catalog/<int:pk>/products/<int:pk2>', ItemDetailsView.as_view(), name='product'),               # Главная страница
    path('catalog/0/search/', ItemSearchView.as_view(), name='search'),               # Главная страница
    path('auth/login/', AuthLoginView.as_view(), name='login'),               # Главная страница
    path('auth/reg/', AuthReginView.as_view(), name='reg'),               # Главная страница
    path('user/cart/', UserCartView.as_view(), name='user_cart'),               # Главная страница
    path('user/cart/add/<int:product_id>', AddToCartView.as_view(), name='add_user_cart'),               # Главная страница
    path('user/cart/update/<int:item_id>', UpdateCartItemView.as_view(), name='update_user_cart'),               # Главная страница
    path('user/cart/remove/<int:item_id>', RemoveFromCartView.as_view(), name='remove_user_cart'),               # Главная страница
    path('user/cart/merge', MergeGuestCartView.as_view(), name='merge_user_cart'),               # Главная страница
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),               # Главная страница
    path('user/outlog/', UserOutlogView.as_view(), name='user_outlog'),               # Главная страница
    path('test/', MyTemplateView.as_view(), name='test'),       # Страница "О проекте"
]
