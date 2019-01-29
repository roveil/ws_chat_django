from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from api.serializers import UserSerializer, MessageSerializer, AuthSerializer
from django.contrib import auth
from django.contrib.auth.models import User
from api.models import Message
from api.permissions import UserAccessPermission, MessagesAccessPermission
from django.middleware import csrf
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import random

class ResultsSetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 200

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserAccessPermission]
    pagination_class = ResultsSetPagination
    parser_classes = [JSONParser,]

    #handle post request
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(True):
            user = User.objects.create_user(**serializer.validated_data)
            auth.login(request, user)
            return HttpResponse(status=201)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created')
    serializer_class = MessageSerializer
    permission_classes = [MessagesAccessPermission]
    pagination_class = ResultsSetPagination
    parser_classes = [JSONParser,]

    def create(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(True):
            if request.data['text'].startswith("/"):
                SlashCommand(request.data['text'], request)
            else:
                Message.objects.create(text=serializer.validated_data['text'], user=request.user)
            return HttpResponse(status=201)

class AuthHandler(APIView):

    parser_classes = [JSONParser,]
    serializer_class = AuthSerializer
    # check is user was authenticated
    def get(self, request):
        context = {'csrftoken': csrf.get_token(request)}
        if request.user.is_anonymous:
            context['auth'] = 'no'
        else:
            context['auth'] = 'yes'
            context['username'] = request.user.username
        return JsonResponse(context)

    #sign in user
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(True):
            user = auth.authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
                context = {'username': user.username, 'email': user.email}
                return JsonResponse(context)
            return HttpResponse(status=400)

    #sign out user
    def delete(self, request):
        if request.user.is_anonymous == False:
            auth.logout(request)
            return HttpResponse(status=200)

class SlashCommand:
    def __init__(self,command,request):
        self.command = command
        if (command == "/roll"):
            self.execute_roll(request)

    def execute_roll(self, request):
        msg="%s %s получает случайное число (0-100): %d" % (request.user.last_name, request.user.first_name, random.randint(0,100))
        Message.objects.create(text=msg, user=request.user)