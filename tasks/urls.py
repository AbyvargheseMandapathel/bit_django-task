from django.urls import path
from .views import (
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskCreateAPIView,
    TaskUpdateAPIView,
    TaskDestroyAPIView,
    CustomTokenObtainPairView,
    SignUpView,
)

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskRetrieveAPIView.as_view(), name='task-detail'),
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='task-update'),
    path('tasks/delete/<int:pk>/', TaskDestroyAPIView.as_view(), name='task-delete'),
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', SignUpView.as_view(), name='signup'),
]

