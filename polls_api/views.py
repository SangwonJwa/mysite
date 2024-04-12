# from django.shortcuts import get_object_or_404, render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status, mixins
# from rest_framework.views import APIView
from polls.models import Question, Vote
from polls_api.permissions import IsOwnerOrReadOnly, IsVoter
from polls_api.serializers import QuestionSerializer, UserSerializer, RegisterSerializer, VoteSeriazlier
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response

# Create your views here.

class VoteList(generics.ListCreateAPIView): 
    serializer_class = VoteSeriazlier
    permissions_classes = [permissions.IsAuthenticated]

    # 아무나 모든 vote를 보면 안되기 때문에 내 vote만 보도록 설정
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)

    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSeriazlier
    permissions_classes = [permissions.IsAuthenticated, IsVoter]

    def perfrom_update(self, serializer):
        serializer.save(voter=self.request.user)



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