from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound


from .models import User, Shop, Product, ProductImage, ProductColor
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    ShopSerializer,
    ProductSerializer,
    ShopCreateSerializer,
    ProductListSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        res = super().partial_update(request, pk, *args, **kwargs)
        if "favorites" in request.data and len(request.data) == 1:
            return Response(f"Successfully updated user's favorites with products: {request.data.get('favorites', [])}.")
        return res

    @action(detail=False, methods=['post'])
    def login(self, request, **kwargs):
        if 'email' not in request.data or 'password' not in request.data:
            return Response(
                {'msg': 'Both email and password fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response(self.serializer_class(user, context={"request": request}).data, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['post'])
    def logout(self, request, **kwargs):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def create(self, request, **kwargs):
        serializer = ShopCreateSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save()
            return Response(
                self.serializer_class(shop, context={"request": request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None, **kwargs):
        shop = Shop.objects.filter(pk=pk)
        if not shop:
            raise NotFound(f"Shop with id '{pk}' not found.")
        shop = shop.first()
        data = ProductListSerializer(shop.products.all(), many=True, context={"request": request}).data
        return Response(data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        else:
            return self.serializer_class

    def _update_images(self, request, pk):
        images = request.FILES.getlist('images')
        product = Product.objects.filter(pk=pk)
        if not product:
            raise NotFound(f"Product with id '{pk}' not found.")
        product = product.first()
        if images:
            product.images.all().delete()
            for image in images:
                product_image = ProductImage.objects.create(image=image, product=product)
                product_image.save()

    def create(self, request, **kwargs):
        images = request.FILES.getlist('images')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            for image in images:
                product_image = ProductImage.objects.create(image=image, product=product)
                product_image.save()
            return Response(self.serializer_class(product, context={"request": request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        self._update_images(request, pk)
        return super().update(request, pk, *args, **kwargs)

    def partial_update(self, request, pk=None,  *args, **kwargs):
        self._update_images(request, pk)
        return super().partial_update(request, pk, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def categories(self, request, **kwargs):
        return Response({category_names[0]: category_names[1] for category_names in Product.CATEGORY_CHOICES})
