from django.urls import path
from .views import *
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    
    path('register/', RegisterAPIView.as_view(), name='register'), # register user, 
    path("login/", TokenObtainPairView.as_view(), name="login"), # login user, 
    path('crud/', TaskAPIView.as_view(), name='crud'), # task- create,readall , 
    path('crud/<str:title_id>/', TaskAPIView.as_view(), name='crud_param'), # taskparam- get,update,delete 
    path('latestTask/', LatestTasksAPIView.as_view(), name='latestTask'), #TaskList
    path('TaskListlimit10/', TaskListlimit10.as_view(), name='TaskListlimit10'), # TaskListlimit10

]
