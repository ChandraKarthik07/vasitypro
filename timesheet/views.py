import logging
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import hashlib
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope ,OAuth2Authentication
from .tests import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
User = get_user_model() 
from drf_social_oauth2.views import ConvertTokenView as OAuthConvertTokenView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
from oauth2_provider.models import AccessToken
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from .models import Timesheet
from .serializers import TimesheetSerializer

logger = logging.getLogger(__name__)


def home(request):
    return HttpResponse("Hello, karthik")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class.request = request
        return super().post(request, *args, **kwargs)


class UserSignupView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomConvertTokenView(OAuthConvertTokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Modify the response content or add user information
        if response.status_code == HTTP_200_OK:
            data = response.data
            access_token = data.get('access_token')
            if access_token:
                try:
                    access_token_obj = AccessToken.objects.get(token=access_token)
                    print(access_token)
                    user = access_token_obj.user_id

                    data['uuid'] = user.hex
                except AccessToken.DoesNotExist:
                    pass

        return response
    

class ProjectAPIView(APIView):
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id=None):
        if project_id is not None:
            # Retrieve details of a specific project
            project = self.get_object(project_id)
            if project is None:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        else:
            # Retrieve all projects without filtering based on the owner
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)


    def post(self, request):
        # Set the owner field to the user making the request
        request.data['owner'] = request.user.id
        print(request.data)
        
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, project_id):
        project = self.get_object(project_id)
        if project is None:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        request.data['owner'] = request.user.id
        serializer = ProjectSerializer(project, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = self.get_object(project_id)
        if project is None:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the project
        if project.owner != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, project_id):
        try:
            if self.request.method in ['PUT', 'DELETE']:
                # Ensure the owner is the authenticated user
                return Project.objects.get(id=project_id, owner=self.request.user)
            else:
                return Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None
        


from .permissions import IsOwnerOrReadOnly  # Import the custom permission class

class TimesheetAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        request.data['owner'] = request.user.id

        serializer = TimesheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set the user to the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, timesheet_id):
        timesheet = self.get_object(timesheet_id)
        if timesheet is None:
            return Response({'error': 'Timesheet not found'}, status=status.HTTP_404_NOT_FOUND)

        # Use partial=True when creating the serializer instance
        serializer = TimesheetSerializer(timesheet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        timesheets = Timesheet.objects.filter(user=request.user)
        serializer = TimesheetSerializer(timesheets, many=True)
        return Response(serializer.data)

    def get_object(self, timesheet_id):
        try:
            timesheet = Timesheet.objects.get(id=timesheet_id)
            self.check_object_permissions(self.request, timesheet)  # Check permissions
            return timesheet
        except Timesheet.DoesNotExist:
            return None