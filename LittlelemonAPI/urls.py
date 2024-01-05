from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.CategoryView.as_view()),
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('menu', views.menu, name='menu'),
    path('', views.welcome, name='welcome'),
    # for class based filtering
    path('filtered-menu-items',
         views.MenuItemsViewSet.as_view({'get': 'list'})),
    path('filtered-menu-items/<int:pk>',
         views.MenuItemsViewSet.as_view({'get': 'retrieve'})),
    path('secret', views.secret, name='secret'),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('manager-view', views.manager_view, name='manager_view'),
    path('throttle-check', views.throttle_check, name='throttle_check'),
    path('throttle-check-auth', views.throttle_check_auth,
         name='throttle_check_auth')
]
