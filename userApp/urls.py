from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, greetingView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('greetings/', greetingView.as_view(), name='greetings')
]