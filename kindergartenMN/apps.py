from django.apps import AppConfig

class KindergartenmnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kindergartenMN'
 
    def ready(self):
        from django.contrib.auth.models import Group
        for group_name in ['Admin', 'Chef', 'Manager']:
            Group.objects.get_or_create(name=group_name) 