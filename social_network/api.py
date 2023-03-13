from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from django.db.models import Q

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return obj == request.user

class ProfileDetail(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        user = User.objects.filter(username=self.kwargs['username'])
        obj = queryset.get(user=user[0])
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class UserDetail(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(username=self.kwargs['username'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class FriendsList(mixins.CreateModelMixin,generics.ListAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs['username'])
        queryset = Friendship.objects.filter(Q(to_user=user[0]) | Q(from_user=user[0]))
        return queryset

    
class PostList(generics.ListAPIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user)
        queryset = Post.objects.filter(user=user[0])
        return queryset
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
