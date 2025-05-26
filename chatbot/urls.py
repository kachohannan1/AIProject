from django.urls import path
from .views import RegisterView, LoginView, ChatMessageView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('messages/', ChatMessageView.as_view(), name='messages'),
]
