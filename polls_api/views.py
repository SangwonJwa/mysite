# from django.shortcuts import get_object_or_404, render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status, mixins
# from rest_framework.views import APIView
from polls.models import Question
from polls_api.permissions import IsOwnerOrReadOnly
from polls_api.serializers import QuestionSerializer, UserSerializer, RegisterSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User

# Create your views here.

# CLASS 기반의 API View / Mixin, GenericAPIView 사용
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # 로그인이 된 상태에서만 question 생성 가능
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # create할 때 owner필드를 현재 접속한 유저로 설정
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer


# 데코레이터 기반의 API View
# @api_view(['GET', 'POST'])
# def question_list(request):
#     if request.method == 'GET':
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many = True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def question_detail(request, id):
#     question = get_object_or_404(Question, pk=id)

#     if request.method == 'GET':
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)