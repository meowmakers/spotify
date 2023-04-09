from .models import CustomUserManager, CustomUser
from .utils import create_activation_code, send_activation_code
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        write_only_fields = ['password']
        
    password_confirm = serializers.CharField()
    
    def validate(self, attrs: dict):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('пароли не совпадают')
        return attrs 
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('такая почта уже существует')
        return email
    
    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        create_activation_code(user)
        send_activation_code(user)
        return user 
    
class ActivationSerializer(serializers.Serializer):
    
    activation_code = serializers.CharField(max_length=10)
    
    def validate_activation_code(self, activation_code):
        if User.objects.filter(activation_code=activation_code).exists():
            return activation_code 
        raise serializers.ValidationError('Неверно указан код')
    
    def activate(self):
        code = self.validated_data.get('activation_code')
        user = User.objects.get(activation_code=code)
        user.is_active = True 
        user.activation_code = ''
        user.save()
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Неверно указан username')
        return username

    def validate(self, attrs):
        request = self.context.get('request')
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(
                username=username,
                password=password,
                request=request
            )
            if not user:
                raise serializers.ValidationError('Неправильно указан логин или пароль')
        else:
            raise serializers.ValidationError('Логин и пароль обязательны к заполнению')
        attrs['user'] = user
        return attrs