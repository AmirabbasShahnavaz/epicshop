from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import TemplateView, ListView

from authentication_module.model import User
from helper_utils.auth import check_user_authenticated
from product_module.model import Product, FavoriteProduct
from user_panel_module.context.change_password import change_password_context
from user_panel_module.context.edit_user import edit_user_context
from user_panel_module.context.enums import ChangePasswordResult
from user_panel_module.forms import EditUserModelForm, ChangePasswordForm


# Create your views here.

class HomeUserView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not check_user_authenticated(request):
            messages.info(request, "برای رفتن به حساب کاربری ابتدا وارد حساب کاربری خود شوید!")
            return redirect('login_page')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'user_panel_module/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeUserView, self).get_context_data()
        context['user'] = User.objects.filter(id=self.request.user.id).first()
        return context


@method_decorator(login_required, name='dispatch')
class EditUserView(View):
    def get(self, request: HttpRequest):
        user: User = get_object_or_404(User, id=self.request.user.id)
        next_url = request.GET.get('next', '')
        return render(request, 'user_panel_module/edit.html',
                      {'form': EditUserModelForm(instance=user), 'user': user, 'next_url': next_url})

    def post(self, request: HttpRequest):
        user: User = get_object_or_404(User, id=self.request.user.id)
        edit_user_model_form = EditUserModelForm(request.POST, request.FILES, instance=user)
        next_url = request.POST.get('next')
        if edit_user_model_form.is_valid():
            edit_user_context(edit_user_model_form)
            messages.success(request, 'حساب کاربری شما با موفقیت ویرایش شد!')
            # for validation host of next_url page
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('user_panel_edit_user_page')
        return render(request, 'user_panel_module/edit.html',
                      {'form': edit_user_model_form})


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        return render(request, 'user_panel_module/change_password.html', {'form': ChangePasswordForm()})

    def post(self, request: HttpRequest):
        user: User = get_object_or_404(User, id=self.request.user.id)
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            result = change_password_context(request, user, change_password_form)
            match result:
                case ChangePasswordResult.success:
                    messages.info(request, ChangePasswordResult.success.value)
                    return redirect('login_page')

                case ChangePasswordResult.error:
                    return render(request, 'user_panel_module/change_password.html',
                                  {'form': change_password_form})

        return render(request, 'user_panel_module/change_password.html', {'form': change_password_form})


@method_decorator(login_required, name='dispatch')
class FavoriteProductListView(ListView):
    model = FavoriteProduct
    context_object_name = 'favorite_products'
    template_name = 'user_panel_module/favorite_products.html'
    paginate_by = 6
    extra_context = {'paging_background': False}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, is_delete=False)
        return queryset

    def post(self, request: HttpRequest):
        favorite_id = request.POST.get('favorite_id')
        favorite_product = FavoriteProduct.objects.filter(user=self.request.user, pk=favorite_id).first()
        if not favorite_product:
            messages.error(request, 'محصولی یافت نشد!')
            return redirect('user_panel_favorite_products_page')
        favorite_product.is_delete = True
        favorite_product.save()
        messages.success(request, 'محصول مورد نظر با موفقیت از لیست علاقه مندی های شما حذف شد!')
        return redirect('user_panel_favorite_products_page')
