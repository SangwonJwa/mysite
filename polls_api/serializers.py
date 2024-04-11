from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from polls.models import Question
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date', 'owner')

class UserSerializer(serializers.ModelSerializer):
    # question들을 가져오는 필드의 정보는 User 테이블에 있는게 아니기 때문에 따로 불러오는 처리가 필요 
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'questions')

class RegisterSerializer(serializers.ModelSerializer):
    # 패스워드에 대한 설정 (validate_password를 이용하여 password의 유효성을 검사)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    # 자체 유효성 검사를 위한 validate 메서드 구현
    def validate(self, attrs):
        if attrs['password']!= attrs['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return attrs

    # User 객체에는 password2 가 없기 때문에 따로 create 메서드 구현
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        