from rest_framework import serializers
from .models import CustomUser,Post

class Userserilizer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confirm_password', 'profile_picture', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password doesnot match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            profile_picture=validated_data.get('profile_picture'),
            bio=validated_data.get('bio')
        )
        return user
    
class Postseriliazer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ['id', 'author', 'caption', 'image', 'created_at']
        read_only_fields = ['id', 'created_at', 'author']   

    def create(self, validated_data):
        user=self.context['request'].user
        post=Post.objects.create(author=user, **validated_data)
        return post


class profiledisplaySerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(use_url=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture']
        
class postdisplaySerializer(serializers.ModelSerializer):
    image_url=serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields =['id','caption','image_url','created_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None   
