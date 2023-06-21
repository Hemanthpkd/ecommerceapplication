from django.shortcuts import render,redirect
from customer.forms import RegistrationForm,LoginForm,ReviewForm
from django.views.generic import View,TemplateView,CreateView,FormView,DetailView,ListView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from store.models import Products,Carts,Orders,Offers
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def signout_view(request,*args,**kwargs):
    logout(request)
    messages.error(request,"logout successfully")
    return redirect("signin")

# class SignUpView(View):
#     def get(self,request,*args,**kwargs):
#         form=RegistrationForm()
#         return render(request,"signup.html",{"form":form})

#     def post(self,request,*args,**kwargs):
#         form=RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("signup")
#         else:
#             return render(request,"signup.html",{"form":form})
class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="signup.html"
    success_url=reverse_lazy("signin")


class SignInView(FormView):
    form_class=LoginForm
    template_name='login.html'
#     def get(self,request,*args,**kwargs):
#         form=LoginForm()
#         return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            # return render(request,"login.html",{"form":form})
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
               
                login(request,usr)
                messages.success(request,"account created seccessfully")
                return redirect("home")
            else:  
                messages.error(request,"provided credentials are invalid")
                return render(request,"login.html",{"form":form})
            
#         

@method_decorator(signin_required,name="dispatch")
# class IndexView(View):
#     def get(self,request,*args,**kwargs):
#         qs=Products.objects.all()
#         return render(request,"index.html",{"products":qs})
class IndexView(ListView):
    model = Products
    template_name = "index.html"
    success_url=reverse_lazy("home")
    context_object_name = "products"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

# class UserprofileView(TemplateView):
    
#     template_name="profile_detail.html"
    
# class ProfileCreateView(CreateView):
#     model=Userprofile
#     form_class=UserprofileForm
#     template_name="userprofile.html"
#     success_url=reverse_lazy("profile_detail")


@method_decorator(signin_required,name="dispatch")   
# class ProductDetailView(View):
#     def get(eslf,request,*args,**kwargs):
#         id=kwargs.get("id")
#         qs=Products.objects.get(id=id)
#         return render(request,"product-details.html",{"product":qs})
class ProductDetailView(DetailView):
    model = Products
    template_name = "product-details.html"
    context_object_name = "product"
    pk_url_kwarg = "id"

@method_decorator(signin_required,name="dispatch")    
class AddToCartView(FormView):
    def post(self,request,*args,**kwargs):
        qty=request.POST.get("qty")
        user=request.user
        id=kwargs.get("id")
        products=Products.objects.get(id=id)
        Carts.objects.create(product=products,user=user,qty=qty)
        return redirect("home")

@method_decorator(signin_required,name="dispatch")
# class CartListView(View):
#     def get(self,request,*args,**kwargs):
#         qs=Carts.objects.filter(user=request.user,status="in-cart")
#         return render(request,"cart-list.html",{"carts":qs})
class CartListView(ListView):
    model = Carts
    template_name = "cart-list.html"
    context_object_name = "carts"

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user, status="in-cart")

@method_decorator(signin_required,name="dispatch")    
class CartRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Carts.objects.filter(id=id).update(status="canceled")
        return redirect("home")

@method_decorator(signin_required,name="dispatch")    
# class MakeOrderView(View):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("id")
#         qs=Carts.objects.get(id=id)
#         return render(request,"checkout.html",{"cart":qs})
class MakeOrderView(DetailView):
    model = Carts
    template_name = "checkout.html"
    context_object_name = "cart"
    pk_url_kwarg = "id"
    
    def post(self,request,*args,**kwargs):
        user=request.user
        address=request.POST.get("address")
        id=kwargs.get("id")
        cart=Carts.objects.get(id=id)
        product=cart.product
        Orders.objects.create(
            product=product,
            user=user,
            address=address,

        )
        cart.status="order-placed"
        cart.save()
        return redirect("home")

@method_decorator(signin_required,name="dispatch")   
class OrderListView(View):
    def get(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user,status="order-placed")
        return render(request,"order-list.html",{"orders":qs})
# class OrderListView(ListView):
#     model = Orders
#     template_name = "order-list.html"
#     context_object_name = "orders"

#     def get_queryset(self):
#         return Orders.objects.filter(user=self.request.user, status="order-placed")

@method_decorator(signin_required,name="dispatch")    
class OrderRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Orders.objects.filter(id=id).update(status="canceled")
        return redirect("order-list")

@method_decorator(signin_required,name="dispatch")    
# class DiscountProductsView(View):
#     def get(self,request,*args,**kwargs):
#         qs=Offers.objects.all()
#         return render(request,"offer-product.html",{"offers":qs})

class DiscountProductsView(ListView):
    model = Offers
    template_name = "offer-product.html"
    context_object_name = "offers"

@method_decorator(signin_required,name="dispatch")   
class RevieCreateView(View):
    def get(self,request,*args,**kwargs):
        form=ReviewForm()
        return render(request,"review-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=ReviewForm(request.POST)
        id=kwargs.get("id")
        pro=Products.objects.get(id=id)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.product=pro
            form.save()
            return redirect("home")
        else:
            return render(request,"review-add.html",{"form":form})