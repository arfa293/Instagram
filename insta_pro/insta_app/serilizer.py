from rest_framework import serializers
from .models import CustomUser,Post,Follow,like,Comment

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
        fields = ['id','username', 'email', 'profile_picture','bio']
        
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
class followserilizer(serializers.ModelSerializer):
    class Meta:
        model=Follow
        fields = ['id', 'follower', 'following', 'created_at']   

class PostViewSerializer(serializers.ModelSerializer):
    author_name=serializers.CharField(source='author.username', read_only=True)
    author_profile_picture = serializers.ImageField(source='author.profile_picture', read_only=True)

    class Meta:
        model=Post
        fields=[ 'id',
            'author_name',
            'author_profile_picture',
            'caption',
            'image',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'author'] 


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=like
        fields=['id', 'post', 'user', 'created_at']     

class CommentRetrieveSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_username', 'user_profile_picture', 'text', 'created_at']

    def get_user_profile_picture(self, obj):
        request = self.context.get('request')
        # Directly access the profile_picture on CustomUser
        if obj.user.profile_picture and request:
            return request.build_absolute_uri(obj.user.profile_picture.url)
        return None

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'text']

    def validate_post(self, value):
        # Ensure that the value is an actual Post object, not an ID
        if not isinstance(value, Post):
            if not Post.objects.filter(id=value).exists():
                raise serializers.ValidationError("Post does not exist")
        return value