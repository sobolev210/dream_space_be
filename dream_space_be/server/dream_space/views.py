from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import RegistrationSerializer, UserSerializer, ShopSerializer, ProductSerializer, ShopCreateSerializer
from .models import User, Shop, Product


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def categories(self, request, **kwargs):
        return Response({category_names[0]: category_names[1] for category_names in Product.CATEGORY_CHOICES})

