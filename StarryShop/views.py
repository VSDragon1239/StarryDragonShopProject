from lib2to3.fixes.fix_input import context

from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView
from .forms import CustomUserRegistrationForm, CustomLoginForm


from StarryShop.ViewModels.CategoriesViewModelModule import CategoriesViewModel
from StarryShop.ViewModels.ProductsViewModelModule import ProductsViewModel
from StarryShop.models import Cart, CartItem, Product


# class User:
#     isAuth = False
#
#     def isAuthenticated(self):
#         return self.isAuth
#
#
# UserTest = User()


# Create your views here.
class MyTemplateView(TemplateView):
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class IndexView(TemplateView):
    template_name = "pages/index.html"
    CategoriesView = None
    ProductsView = None
    categories = None
    products = None

    def get(self, request, *args, **kwargs):
        self.initViewModel()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.initViewModel()
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.username == '':
            context['user'] = False
        else:
            context['user'] = user
        context["categories"] = self.categories
        context["products"] = self.products
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context

    def initViewModel(self):
        self.CategoriesView = CategoriesViewModel()
        self.ProductsView = ProductsViewModel()
        self.categories = self.CategoriesView.get_categories()
        self.products = self.ProductsView.get_products()


class ItemDetailsView(TemplateView):
    template_name = "pages/item_details.html"
    CategoriesView = None
    ProductsView = None
    category_id = None
    product_id = None
    categories = None
    products = None
    product = None

    def get(self, request, *args, **kwargs):
        self.initViewModel()
        self.category_id = kwargs.get('pk')
        print(self.category_id)
        self.product_id = kwargs.get('pk2')
        print(self.product_id)
        self.products = self.ProductsView.get_products(self.category_id)
        self.product = self.ProductsView.get_product(self.product_id)
        print(self.products, self.product.name, self.product.category)
        return self.render_to_response({
            'pk': self.category_id,
            'pk2': self.product_id,
            'products': self.products,
            'product': self.product,
        })

    def get_context_data(self, **kwargs):
        self.initViewModel()
        pk = kwargs.get('pk')  # Получаем значение pk
        pk2 = kwargs.get('pk2')  # Получаем значение pk2
        added_product = kwargs.get('added_product')  # Получаем значение pk2
        quantity = kwargs.get('quantity')  # Получаем значение pk2
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.username == 'AnonymousUser':
            context['user'] = False
        else:
            context['user'] = user
        context["product"] = self.product
        context["pk"] = pk
        context["pk2"] = pk2
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context

    def initViewModel(self):
        self.CategoriesView = CategoriesViewModel()
        self.ProductsView = ProductsViewModel()


class ItemSearchView(TemplateView):
    template_name = "pages/item_search.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.username == '':
            context['user'] = False
        else:
            context['user'] = user
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class UserCartView(TemplateView):
    template_name = "pages/user_cart.html"

    def get(self, request, *args, **kwargs):
        self.cart = self.get_cart(request)
        self.items = self.cart.items.all()
        # print(self.items[0], self.items[0].product.image)
        self.total_price = sum(item.product.price * item.quantity for item in self.items)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.items
        context['total_price'] = self.total_price
        return context

    def get_cart(self, request):
        """Получение текущей корзины"""
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart


class AddToCartView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart = UserCartView().get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        referer_url = request.META.get('HTTP_REFERER', '/')

        # Проверяем, является ли запрос AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'redirect_url': referer_url})

        # Добавляем параметр в путь
        redirect_url = f"{referer_url}?added_product={product.id}&quantity={cart_item.quantity}"
        return redirect(redirect_url)


class UpdateCartItemView(TemplateView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        cart = UserCartView().get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
        return JsonResponse({'status': 'success', 'message': 'Количество обновлено'})


class RemoveFromCartView(TemplateView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        cart = UserCartView().get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        # Получаем URL предыдущей страницы
        referer_url = request.META.get('HTTP_REFERER', '/')

        # Проверяем, является ли запрос AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'redirect_url': referer_url})

        return redirect(referer_url)


class MergeGuestCartView(TemplateView):
    """Объединение гостевой корзины с пользовательской при входе"""
    def merge_carts(self, user, session_key):
        guest_cart = Cart.objects.filter(session_key=session_key).first()
        if guest_cart:
            user_cart, _ = Cart.objects.get_or_create(user=user)
            for item in guest_cart.items.all():
                user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                if not created:
                    user_item.quantity += item.quantity
                user_item.save()
            guest_cart.delete()


class AuthLoginView(TemplateView):
    template_name = "pages/auth_login.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.username == '':
            context['user'] = False
        else:
            context['user'] = user
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')  # Перенаправление на главную страницу
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
        return render(request, self.template_name, {'form': form})


class AuthReginView(TemplateView):
    template_name = "pages/auth_registration.html"

    def get(self, request, *args, **kwargs):
        form = CustomUserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.username == '':
            context['user'] = False
        else:
            context['user'] = user
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context

    def post(self, request):
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('main')  # Перенаправление на главную страницу
        return render(request, self.template_name, {'form': form})


# class UserCartView(TemplateView):
#     template_name = "pages/user_cart.html"
#
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = UserTest.isAuthenticated
#         context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#         return context


class UserProfileView(TemplateView):
    template_name = "pages/user_profile.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user  # Текущий пользователь
        if user.username == '':
            print(user)
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Текущий пользователь
        if user.username == '':
            context['user'] = False
        else:
            context['user'] = user
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class UserOutlogView(TemplateView):
    template_name = "pages/user_outlog.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main')  # Перенаправление после выхода

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = UserTest.isAuthenticated
    #     return context
