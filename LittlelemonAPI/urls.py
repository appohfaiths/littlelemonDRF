from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.CategoryView.as_view()),
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('menu', views.menu, name='menu'),
    path('', views.welcome, name='welcome')
]
