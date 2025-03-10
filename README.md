# TaskManager-crud
  assessment-test CRUD operation with middleware(authentication)

# Project cloning and deployment 
  activate .venv using on windows -> .\.venv\Scripts\activate
  install pip packages using -> pip install -r requirements.txt
# cd Project
  check the database creation on mysql server
  python manage.py makemigrations
  python manage.py migrate

# to run server 
  python manage.py runserver

# to test 
  python manage.py test

# user - 
  created for the foreignkey reference with - authenticated user  
# user1 creates -> 
  {"username":"raji","password":"userraji123"} 
# sample jwt token is -> 
  {eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNjMxMDI3LCJpYXQiOjE3NDE2MjM4MjcsImp0aSI6IjAwNTg4ZTA0ZDQ5MDQyODg5ODU3MzNkNDEyOTVkMWNiIiwidXNlcl9pZCI6Nn0.PheANrC_iDC5aPt0O8Pxa5i91MNGGYEaekaxkv3UP_k  }
# user1 created task as -> 
    each user can be able to create multiple task -> titles and they can access using 'title_id'
  {"title":"api development","description":"created using django restframework"}
  {"title":"frontend application","description":"using react ui designed"}

# for docs checkout:
     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),     # API Schema (JSON)    
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Swagger UI    
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),    # Redoc UI

