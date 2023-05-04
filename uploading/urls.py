from django.urls import path
from .views import *

urlpatterns = [
    path('', Upload.as_view(), name='upload_data'),
    path('check_order/', TaskGetter.as_view()),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]