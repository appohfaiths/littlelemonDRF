from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework import generics, viewsets
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from .throttles import TenCallsPerMinute

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

        # pagination
        perpage = self.request.query_params.get('perpage', default=2)
        page = self.request.query_params.get('page', default=1)

        paginator = Paginator(queryset, per_page=perpage)

        try:
            queryset = paginator.page(number=page)
        except EmptyPage:
            queryset = []

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"menu_items": serializer.data})


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# Class based filtering


class MenuItemsViewSet(viewsets.ModelViewSet):
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']

    # checking for throttling on post calls
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]


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


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only Manager should see this"})
    else:
        return Response({"message": "You are not authorised to see this"}, 403)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "Successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message": "message for logged in users only"})
