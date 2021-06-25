from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from .import views

app_name = 'main'

urlpatterns = [
    path('data/', csrf_exempt(views.DataList.as_view())),
    path('data/<int:pk>', csrf_exempt(views.DataDetail.as_view())),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('success/', views.SuccessView.as_view(), name='success_view'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
