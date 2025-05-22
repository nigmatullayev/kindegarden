from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdminGroupOrSuperuser

class UserListAPIView(APIView):
    permission_classes = [IsAdminGroupOrSuperuser]
    def get(self, request):
        User = get_user_model()
        users = User.objects.all()
        data = []
        for u in users:
            role = u.groups.first().name if u.groups.exists() else ''
            data.append({
                'username': u.username,
                'email': u.email,
                'role': role
            })
        return Response(data) 