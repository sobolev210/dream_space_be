from rest_framework import serializers
from .models import User, Shop, Product, ProductImage, ProductColor
from rest_framework.exceptions import NotFound


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

    def get_logo(self, shop):
        request = self.context.get('request')
        logo_url = shop.logo.url
        return request.build_absolute_uri(logo_url)

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data["logo"] = request.build_absolute_uri(data["logo"])
        return data


class ShopCreateSerializer(ShopSerializer):
    user_id = serializers.IntegerField(min_value=1)

    def save(self):
        user_id = self.validated_data.pop("user_id")
        user = User.objects.filter(id=user_id)
        if not user:
            raise NotFound(f"User with id '{user_id}' not found.")
        user = user.first()
        shop = Shop(**self.validated_data)
        shop.save()
        user.shops.add(shop)
        user.save()
        return shop


#for returning shops inside user
class UserShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["name", "logo"]

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data["logo"] = request.build_absolute_uri(data["logo"])
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            "username"
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data["shops"] = UserShopSerializer(
            Shop.objects.filter(id__in=data.get("shops", [])),
            many=True,
            context={"request": request}
        ).data
        return data


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data["image"] = request.build_absolute_uri(data["image"])
        return data


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

    def save(self, **kwargs):
        product = super().save(**kwargs)
        colors = self.validated_data.get("colors", [])
        for color in colors:
            product_color = ProductColor.objects.create(color=color, product=product)
            product_color.save()
        return product

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data["images"] = ProductImageSerializer(instance.images.all(), many=True, context={"request": request}).data
        data["colors"] = instance.colors.values_list("color", flat=True)
        return data

