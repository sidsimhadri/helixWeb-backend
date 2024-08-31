from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Associate the logged-in user

    def post(self, request, *args, **kwargs):
        logger.debug(f"POST /api/questions/ - Request data: {request.data}")
        return super().post(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

@csrf_exempt
def upvote_question(request, id):
    if request.method == 'PUT':
        logger.debug(f"PUT /api/questions/{id}/upvote - Request data: {request.body}")
        question = get_object_or_404(Question, id=id)
        question.thumbs_up += 1
        question.save()
        return JsonResponse({'thumbs_up': question.thumbs_up})
    logger.warning(f"Invalid request method for upvote_question: {request.method}")
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def downvote_question(request, id):
    if request.method == 'PUT':
        logger.debug(f"PUT /api/questions/{id}/downvote - Request data: {request.body}")
        question = get_object_or_404(Question, id=id)
        question.thumbs_down += 1
        question.save()
        return JsonResponse({'thumbs_down': question.thumbs_down})
    logger.warning(f"Invalid request method for downvote_question: {request.method}")
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug(f"POST /api/register/ - Request data: {data}")
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'message': 'Username and password are required'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username already exists'}, status=400)
            user = User.objects.create_user(username=username, password=password)
            user_data = UserSerializer(user).data
            return JsonResponse({
                'message': 'User created successfully',
                'user': user_data
            })
        except json.JSONDecodeError:
            logger.error("Invalid JSON in register_view")
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
    logger.warning(f"Invalid request method for register_view: {request.method}")
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.debug(f"POST /api/login/ - Request data: {data}")
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            user_data = UserSerializer(user).data
            return JsonResponse({
                'message': 'Login successful',
                'user': user_data
            })
        else:
            logger.warning("Invalid credentials in login_view")
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    logger.warning(f"Invalid request method for login_view: {request.method}")
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logger.debug("POST /api/logout/")
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    logger.warning(f"Invalid request method for logout_view: {request.method}")
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def get_all_users(request):
    if request.method == 'GET':
        logger.debug("GET /api/users/")
        users = User.objects.all().values('id', 'username')
        return JsonResponse(list(users), safe=False)
    logger.warning(f"Invalid request method for get_all_users: {request.method}")
    return JsonResponse({'message': 'Invalid request method'}, status=405)