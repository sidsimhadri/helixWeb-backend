from django.urls import path
from .views import QuestionListCreate, QuestionDetail, upvote_question, downvote_question, register_view, login_view, logout_view, get_all_users

urlpatterns = [
    path('questions/', QuestionListCreate.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('questions/<int:id>/upvote/', upvote_question, name='upvote_question'),
    path('questions/<int:id>/downvote/', downvote_question, name='downvote_question'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', get_all_users, name='get_all_users'),
]
