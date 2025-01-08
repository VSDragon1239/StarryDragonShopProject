from lib2to3.fixes.fix_input import context

from django.shortcuts import render

from django.views.generic import TemplateView


class User:
    def isAuthenticated(self):
        return True


UserTest = User()


# Create your views here.
class MyTemplateView(TemplateView):
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class IndexView(TemplateView):
    template_name = "pages/index.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserTest.isAuthenticated
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class ItemSearchView(TemplateView):
    template_name = "pages/item_search.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserTest.isAuthenticated
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class AuthLoginView(TemplateView):
    template_name = "pages/auth_login.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserTest.isAuthenticated
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class AuthReginView(TemplateView):
    template_name = "pages/auth_registration.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserTest.isAuthenticated
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class UserCartView(TemplateView):
    template_name = "pages/user_cart.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserTest.isAuthenticated
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class UserProfileView(TemplateView):
    template_name = "pages/user_profile.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserTest.isAuthenticated
        context['list_test'] = [1, 2, 3, 4, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        return context


class UserOutlogView(TemplateView):
    template_name = "pages/user_outlog.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserTest.isAuthenticated
        return context
