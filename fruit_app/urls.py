from . import views
from django.urls import path

app_name = 'fruit_app'
urlpatterns = [
    path('',views.index, name='index'),
    path('contact/',views.contact, name='contact'),
    path('shop/',views.shop, name='shop'),
    path('checkout/',views.checkout, name='checkout'),
    path('testimonials/',views.testimonials, name='testimonials'),
    path('cart/',views.cart, name='cart'),
    path('page404/',views.page404, name='404'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('register/',views.register_user, name='register'),
    path('delete/<int:id>',views.delete_order, name='delete_order'),
    path('update/<int:id>',views.update_order, name='update_order'),
    path('description/<int:id>',views.description, name='description'),
    path('add/', views.add_product, name='add_product'),
    path('remove/<int:product_id>/', views.remove_product, name='remove_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    
    
    
    path('pay/',views.pay, name='pay'),
    path('stk/',views.stk, name='stk'),
    path('token/',views.token, name='token'),
] 
