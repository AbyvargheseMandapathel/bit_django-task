from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairSerializer , UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskUpdateAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TaskDestroyAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
    
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)