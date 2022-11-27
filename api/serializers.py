from api.models import post, Comments
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]

    # def create(self, validated_data):
    #
    #     return Comments.objects.create(**validated_data)

class postSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    # liked_by=UserSerializer(many=True,read_only=True)
    likes_count=serializers.CharField(read_only=True)

    class Meta:
        model = post
        exclude = ("date",)

    def create(self, validated_data):
        user = self.context.get('usr')
        return User.objects.create_user(**validated_data, user=user)

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=120)
    password=serializers.CharField(max_length=120)

class CommentsSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields=["comment","user"]
    def create(self,validated_data):
        user=self.context.get("user")
        pst=self.context.get("post")
        return Comments.objects.create(**validated_data,user=user,post=post)



