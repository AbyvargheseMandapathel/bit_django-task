from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token  # Import Token model
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.task1 = Task.objects.create(title="Task 3", description="Description 3", due_date="2024-02-28", status="Pending", owner=self.user)
        self.task2 = Task.objects.create(title="Task 2", description="Description 2", due_date="2024-03-15", status="Completed", owner=self.user)

    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

    def test_task_list_authenticated(self):
        self.authenticate_user() 
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_task_retrieve_authenticated(self):
        self.authenticate_user()  
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 3')

    def test_task_create_authenticated(self):
        self.authenticate_user()  
        url = reverse('task-create')
        data = {
            "title": "New Task",
            "description": "New Task Description",
            "due_date": "2024-03-30",
            "status": "Pending"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_task_update_owner_only(self):
        self.authenticate_user() 
        url = reverse('task-update', kwargs={'pk': self.task1.pk})
        data = {
            "title": "Updated Task",
            "description": "Updated Task Description",
            "due_date": "2024-04-15",
            "status": "Completed"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_task_partial_update_owner_only(self):
        self.authenticate_user() 
        url = reverse('task-update', kwargs={'pk': self.task1.pk})
        data = {
            "title": "Updated Task"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_task_delete_owner_only(self):
        self.authenticate_user()  
        url = reverse('task-delete', kwargs={'pk': self.task1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
