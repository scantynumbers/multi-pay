from re import match
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from transaction.models import Transaction
from user.models import UserApiKey

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registeration"""
    password = serializers.CharField(
        max_length=255,
        required=True,
        style={"input_type": "password"},
        write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        required=True,
        style={"input_type": "password"},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone_number', 'password', 'password2']

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                "A user with this email allready exists")
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError("Passwords do not match")

        try:
            password_validation.validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ApiKeySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField()

    class Meta:
        model = UserApiKey
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):
    PAYMENT_CHOICES = (
        ('PAYPAL', 'paypal'),
        ('PAYSTACK', 'paystack'),
        ('STRIPE', 'stripe'),
        ('FLUTTERWAVE', 'rave_payment'),
        ('CRYPTO', 'crypto')

    )
    CURRENCY_CHOICES = (
        ('NGN', 'ngn'),
        ('USD', 'usd'),
        ('EUR', 'eur'),
        ('CAD', 'cad'),
        ('BTC', 'btc')

    )
    description = serializers.CharField(
        max_length=255, required=False)
    platform = serializers.ChoiceField(choices=PAYMENT_CHOICES)
    title = serializers.CharField(
        max_length=255, required=False)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    currency = serializers.CharField(
        max_length=4, choices=CURRENCY_CHOICES, default='NGN')
    logo = serializers.URLField(required=False)
