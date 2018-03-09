from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView,
    CreateAPIView, RetrieveUpdateAPIView,
    )
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from posts.models import Post
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import PostListSerializer, PostDetailSerializer, PostCeateSerializer
from .permissions import IsOwnerOrReadOnly

class PostListAPIView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter,    # 通过search查询过滤
                       OrderingFilter]  # 通过ordering查询过滤
    search_fields = ['title', 'content', 'user__first_name']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')  # 通过q查询过滤
        if query:
            queryset_list = queryset_list.filter(title__icontains=query)
        return queryset_list


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCeateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # 将user从创建者变为更变者
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'