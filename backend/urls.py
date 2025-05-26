from django.urls import path
from chatbot.views import RegisterView, LoginView, ChatMessageView, PredictView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/chatmessages/', ChatMessageView.as_view(), name='chatmessages'),
    path('api/predict/', PredictView.as_view(), name='predict'),
]
