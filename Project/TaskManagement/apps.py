from django.apps import AppConfig


class TaskmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TaskManagement'

    def ready(self):
        import TaskManagement.signals