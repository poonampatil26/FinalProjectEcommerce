from django.urls import path
from . import views


urlpatterns=[
    path('',views.homeview, name='home'),
    path('seller_to_customer_home', views.seller_to_customer_home, name='seller_to_customer_home'),

    path('showlaptop/',views.showlaptop, name='showlaptop'),
    path('showmobile/', views.showMobile, name='showmobile'),
    path('showgrocery/', views.showGrocery, name='showgrocery'),
    path('customerlaptopitem/<int:pk>', views.Laptopview, name='customerlaptopitem'),
    path('customermobileitem/<int:pk>', views.Mobileview, name='customermobileitem'),
    path('customergroceryitem/<int:pk>', views.Groceryview, name='customergroceryitem'),

    path('cartview/', views.Cartview, name='cartview'),
    path('deleteitem/<int:pk>', views.Deleteitemview, name='deleteitem'),
    path('customerupdateitem/<int:pk>', views.Updateallitemview, name='customerupdateitem'),
    path('createprofile/',views.create_profile,name='createprofile'),
    path('updateprofile/<int:id>/',views.update_profile,name='updateprofile'),
    path('showprofile/',views.show_profile,name='showprofile'),
    path('profilepage/',views.profile_page,name='profilepage'),
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('showaddress/',views.show_addresses,name='showaddress'),
    path('updateaddress/<int:pk>/',views.CustomerAddressUpdateView.as_view(),name='updateaddress'),
    path('deleteaddress/<int:id>/',views.delete_address,name='deleteaddress'),
    path('createaddress/',views.create_address,name='createaddress'),


   

]
