from rest_framework import serializers
from rest_framework.serializers import  Serializer
from django.contrib.auth import get_user_model

User = get_user_model()



class UserAccountSerializer(Serializer):
  """ Serializer is used to create and login user credentials """
  
  email = serializers.CharField()
  password  = serializers.CharField(max_length = 20, required =True)



  def validate_password(self, value):
    if value =='dineshsingh':
      raise serializers.ValidationError('Password must be at least 6 characters long')
    return value
 
  def create(self, validated_data):
    
    return User.objects.create_user(**validated_data)



class ResetPasswordSerializer(Serializer):
  """ Serializer is used to deserialized the incoming password reset data """
  email = serializers.EmailField()
  password = serializers.CharField(max_length = 50)
  otp  = serializers.CharField(max_length = 4)


