from django.shortcuts import render
from rest_framework.viewsets import  ViewSet,ModelViewSet
from rest_framework.views import APIView
from api.serializers import postSerializer,UserSerializer,LoginSerializer,CommentsSerializer
from rest_framework.response import Response
from api.models import post
from django.contrib.auth import authenticate
from rest_framework import authentication,permissions
from rest_framework.decorators import action

class PostView(ViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request,*args,**kwargs):
        qs=post.objects.all()
        serializer=postSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kwargs):
        serializer=postSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=post.objects.get(id=id)
        serializer=postSerializer(qs)
        return Response(data=serializer.data)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=post.objects.get(id=id)
        serializer=postSerializer(instance=instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=post.objects.get(id=id)
        instance.delete()
        return Response({"msg":"deleted"})

class UserView(ViewSet):
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            uname=serializer.validated_data.get("username")
            pwd=serializer.validated_data.get("password")
        return Response

class PostModelView(ModelViewSet):
    serializer_class = postSerializer
    queryset =post.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        user=request.user
        serializer=postSerializer(data=request.data,context={"usr":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

    @action(methods=["GET"],detail=False)
    def my_post(self,request,*args,**kwargs):
        user=request.user
        qs=user.posts.all()
        serializer=postSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"], detail=True)
    def get_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Post=post.objects.get(id=id)
        cmts=Post.comments_set.all()
        serializer=CommentsSerializer(cmts,many=True)
        return Response(data=serializer.data)

    @action(methods=["POST"],detail=True)
    def add_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=post.objects.get(id=id)
        serializer=CommentsSerializer(data=request.data,context={"user":request.user,"post":pst})
        if serializer.is_valid():
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        # cmts=request.data.get("comment")
        # pst.comments_set.create(comment=cmts,user=request.user)
        # return Response(data="ok")

    @action(methods=["POST"],detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=post.objects.get(id=id)
        user=request.user
        pst.liked_by.add(user)
        return Response(data="ok")

    @action(methods=["GET"],detail=True)
    def get_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=post.objects.get(id=id)
        count=pst.liked_by.all().count()
        return Response(data=count)