from rest_framework import serializers
from .models import Residentsdata, Vehiclesdata, User, Guard
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # Include fields relevant to your use case
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
        

class ResidentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Residentsdata
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        # Check if a User with the same username already exists
        try:
            user = User.objects.create_user(**user_data)
        except IntegrityError:
            raise serializers.ValidationError({'user': 'A user with this username or email already exists.'})
        
        resident = Residentsdata.objects.create(user=user, **validated_data)
        return resident

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiclesdata
        fields = '__all__'



class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guard
        fields = '__all__'

    