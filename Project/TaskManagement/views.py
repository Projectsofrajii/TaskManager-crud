from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist

import functools
# Create your views here.

class TaskPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow anyone to register

# Exception Handling Decorator
def handle_exceptions(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except IntegrityError as e:
            return Response({"error": "Integrity error: Constraint violation", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ProgrammingError as e:
            return Response({"error": "Database programming error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper

class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Allow only authenticated users
    pagination_class = TaskPagination  # Apply pagination

    @handle_exceptions
    def get(self, request, *args, **kwargs):
        """Retrieve a single Task by title_id or list all Tasks"""
        title_id = kwargs.get('title_id')
        if title_id:
            task = get_object_or_404(Task, title_id=title_id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        tasks = Task.objects.only("title_id",  "title","description","status")
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @handle_exceptions
    def post(self, request, *args, **kwargs):
        """Create a new Task"""
        data = request.data.copy()
        data["user"] = request.user.id  # Assign logged-in user

        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)  # Auto-raises ValidationError if invalid
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @handle_exceptions
    def put(self, request, *args, **kwargs):  
        """Update an entire Task"""
        title_id = kwargs.get('title_id')
        task = get_object_or_404(Task, title_id=title_id)

        data = request.data.copy()
        data["user"] = request.user.id  

        serializer = TaskSerializer(task, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @handle_exceptions
    def patch(self, request, *args, **kwargs):  
        """Partially update a Task"""
        title_id = kwargs.get('title_id')
        task = get_object_or_404(Task, title_id=title_id)

        data = request.data.copy()
        data["user"] = request.user.id  

        serializer = TaskSerializer(task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @handle_exceptions
    def delete(self, request, *args, **kwargs):  
        """Delete a Task"""
        title_id = kwargs.get('title_id')
        task = get_object_or_404(Task, title_id=title_id)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LatestTasksAPIView(APIView): 
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination  # Apply pagination

    @handle_exceptions
    def get(self, request):
        paginators = self.pagination_class ()
        tasks = Task.objects.only("title", "created_at").order_by('-created_at')  
        pages = paginators.paginate_queryset(tasks,request, view=self) 
        serializer = TaskSerializer(pages,many=True)
        return paginators.get_paginated_response(serializer.data)
    
class TaskListlimit10(APIView): # this is problematic question so applied limit 10
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination  # Apply pagination

    @handle_exceptions
    def get(self, request):
        """Retrieve the latest 10 tasks sorted by created_at"""
        tasks = Task.objects.only("title", "created_at").order_by('-created_at')[:10]  # **Optimization: Select & Order by created_at**
        return Response(
            [{"title": task.title, "created_at": task.created_at} for task in tasks], 
            status=status.HTTP_200_OK
        )
    
