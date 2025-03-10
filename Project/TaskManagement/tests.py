from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task  # Import the Task model


class TaskAPITestCase(APITestCase):
    """Test case for Task API"""

    def setUp(self):
        """Setup test data before each test"""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpass', email="test@gmail.com"
        )

        # Authenticate user
        self.client.force_authenticate(user=self.user)

        # Create a test task
        self.task = Task.objects.create(
            title="Sample Task",
            description="Task for testing",
            title_id="TID123",  # Ensure title_id is explicitly set
            user=self.user
        )

        # Update the base URL to match urls.py
        self.base_url = "/crud/"

    def test_create_task(self):
        """Test creating a new task with auto-generated title_id"""
        data = {
            "title": "New Task",
            "description": "Testing creation"
        }

        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch the latest created task and verify title_id
        new_task = Task.objects.get(title="New Task")
        self.assertTrue(new_task.title_id.startswith("TID"))

    def test_get_all_tasks(self):
        """Test retrieving all tasks"""
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Ensure at least one task exists

    def test_get_task_by_title_id(self):
        """Test retrieving a specific task by title_id"""
        url = f"{self.base_url}{self.task.title_id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title_id"], self.task.title_id)

    def test_update_task(self):
        """Test updating an existing task (PUT)"""
        url = f"{self.base_url}{self.task.title_id}/"

        data = {
            "title": "Updated Task",
            "description": "Updated description"
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Task")

    def test_partial_update_task(self):
        """Test partially updating a task (PATCH)"""
        url = f"{self.base_url}{self.task.title_id}/"

        data = {"description": "Partially updated description"}

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Partially updated description")

    def test_delete_task(self):
        """Test deleting a task"""
        url = f"{self.base_url}{self.task.title_id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(title_id=self.task.title_id).exists())
