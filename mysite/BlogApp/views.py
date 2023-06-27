from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserRegistrationAPIView(APIView):
    
    def post(self, request):
        context = {}
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context['status'] = '200'
                context['status_message'] = 'OK'
                context['data'] = serializer.data
            else:
                context['status'] = '400'
                context['status_message'] = 'BAD REQUEST'
                context['data'] = ''
            return Response(context)
        except Exception as e:
            context['status'] = '400'
            context['status_message'] = str(e)
            context['data'] = ''
            return Response(context)

class LoginAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        context = {}
        user = request.user
        try:
            user_object = User.objects.get(username=user)
            blog_object = Post.objects.filter(user=user_object)
            if len(blog_object) > 0:
                serializer =  BlogSerializer(blog_object,many=True)
                context['status'] = '200'
                context['status_message'] = 'OK'
                context['data'] = serializer.data
            else:
                context['status'] = '400'
                context['status_message'] = 'No Blogs found for this user'
                context['data'] = ''
        except Exception as e:
            context['status'] = '400'
            context['status_message'] = 'BAD REQUEST'
            context['data'] = ''

        return Response(context)

    def post(self,request):
        context = {}
        user = request.user
        user_object = User.objects.get(username=user)
        data = request.data
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            context['status'] = '200'
            context['status_message'] = 'OK'
            context['data'] = serializer.data
        else:
            context['status'] = '400'
            context['status_message'] = 'BAD REQUEST'
            context['data'] = ''
        return Response(context)
   




class Blogupdatedelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def put(self,request,pk):
        context = {}
        user = request.user
        try:
            user_object = User.objects.get(username=user)
            blog_object = Post.objects.get(id=pk)
            if blog_object.user == user_object:
                blog_serializer = BlogSerializer(blog_object,data=request.data)
                if blog_serializer.is_valid():
                    context['status'] = '200'
                    context['status_message'] = 'OK'
                    context['data'] = blog_serializer.data
                else:
                    context['status'] = '400'
                    context['status_message'] = 'BAD REQUEST'
                    context['data'] = ''
            else:
                context['status'] = '400'
                context['status_message'] = "User don't have appropriate permission to access the resource"
                context['data'] = ''
        except Exception as e:
            context['status'] = '400'
            context['status_message'] = "BAD REQUEST"
            context['data'] = ''

        return Response(context)
    def delete(self,request,pk):
        context = {}
        try:
            blog_object = Post.objects.get(id=pk)
            if blog_object:
                blog_object.delete()
                context['status'] = '200'
                context['status_message'] = "Blog is deleted successfully"
                context['data'] = ''
            else:
                context['status'] = '400'
                context['status_message'] = "Blog not found"
                context['data'] = ''
        except Exception as e:
             context['status'] = '400'
             context['status_message'] = "Blog not found"
             context['data'] = ''

        return Response(context)
   
        
