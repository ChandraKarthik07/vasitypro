from django.urls import path, include, re_path
from .views import *
urlpatterns = [

    path('signup/', UserSignupView.as_view(), name='signup'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('oauth2/convert-token/', CustomConvertTokenView.as_view(), name='convert_token'),
    path('projects/', ProjectAPIView.as_view(), name='project-crud'),
    path('projects/<int:project_id>/', ProjectAPIView.as_view(), name='project-crud'),

]

urlpatterns += [
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf'))
]
