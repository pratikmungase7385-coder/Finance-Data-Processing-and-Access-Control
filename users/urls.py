from django.urls import path
from .views import MeView, UserListCreateView, UserDetailView
from .views import RegisterView
from .views import RegisterView, LoginView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view(), name='user-me'),
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view()), 
]
