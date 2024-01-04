from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer

# Create your views here.


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.all()

        # Filtering by category name
        category_name = self.request.query_params.get('category')
        if category_name:
            queryset = queryset.filter(category__title=category_name)

        # Filtering by price
        to_price = self.request.query_params.get('to_price')
        if to_price:
            queryset = queryset.filter(price__lte=to_price)

        # Searching
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # Ordering
        ordering = self.request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            queryset = queryset.order_by(*ordering_fields)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"menu_items": serializer.data})


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)


@api_view()
# @renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(
        items, many=True, context={'request': request})
    return Response({'data': serialized_item.data}, template_name='menu.html')


@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)
