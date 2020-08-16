from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
urlpatterns = [
     path('', views.home,name="home"),
     path('product/',views.products,name="product"),
     path('customer/<str:pk>/',views.customer_view,name="customer"),

     path('createorder/<str:pk>', views.createorder,name="create_order"),
     path('updateform/<str:pk>', views.updateorder,name="update_order"),
     path('delete/<str:pk>/', views.deleteorder,name="delete_order"),

     path('customercreate/', views.createcustomer,name="create_customer"),
     path('updatecustomer/<str:pk>', views.updatecustomer,name="update_customer"),
     path('deletecustomer/<str:pk>', views.deletecustomer,name="delete_customer"),

      path('register',views.registerpage,name="register"),
      path('login',views.loginpage,name="login"),
      path('logout',views.logoutuser,name='logout'),
      path('userrcalling/',views.user_page_view,name='user-page'),
      path('accountsettings/',views.accountsettings,name='account-settings'),

    #for passoword change
      path('reset_password/',auth_view.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
      name="reset_password"), #alreadydefined view in documentation,class based views
      path('reset_passowrd_sent/',auth_view.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html')
      ,name="password_reset_done"),
      path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html')
      ,name="passowrd_reset_confirm"),
      path('reset_password_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html')
      ,name="password_reset_complete"),
 
    ]
