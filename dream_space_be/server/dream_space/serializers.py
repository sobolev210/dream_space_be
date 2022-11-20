from rest_framework import serializers
from .models import User, Shop


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


#for returning shops inside user
class UserShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["name", "logo"]


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

    #todo return full path for logo
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["shops"] = UserShopSerializer(
            Shop.objects.filter(id__in=data.get("shops", [])),
            many=True
        ).data
        return data
