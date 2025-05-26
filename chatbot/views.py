from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import ChatMessage
from .serializers import RegisterSerializer, UserSerializer, ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated users to register

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]  # Also allow anyone to login

    def post(self, request):
        # Change here: pass email instead of username to authenticate
        user = authenticate(request, email=request.data.get('email'), password=request.data.get('password'))
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=400)

class ChatMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access chat messages

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def get(self, request):
        messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')
        return Response(ChatMessageSerializer(messages, many=True).data)

class PredictView(APIView):
    permission_classes = [IsAuthenticated]  # Or AllowAny if no auth needed

    def post(self, request):
        user_input = request.data.get('message', '')
        
        # Example: simple echo or integrate your AI/model logic here
        prediction = f"Predicted response for: {user_input}"

        return Response({"prediction": prediction})