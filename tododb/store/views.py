from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Tasks
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView


class CreateNewTaskAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTasksAPIView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(user=user)


class UpdateTaskApiView(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTaskApiView(DestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)
