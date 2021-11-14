from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title, User

from .permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthor, IsModerator,
                          IsSuperuser)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterSerializer,
                          ReviewSerializer, TitleReadSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserSerializer)
from .viewsets import CreateListDestroyViewset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsSuperuser | IsAdmin,)
    lookup_field = 'username'

    @action(methods=['PATCH', 'GET'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me')
    def get_me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            self.request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_view(request):
    """Сервис Yamdb получает данные от пользователя и отправляет на почту код
       подтверждения"""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(User, email=serializer.validated_data['email'])
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    email = settings.EMAIL_HOST_USER
    send_mail(
        subject=subject,
        message=message,
        from_email=email,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes((AllowAny,))
def token_view(request):
    """Пользователь отправляет POST-запрос с кодом подтверждения, и в ответ
       получает JWT-токен"""
    if request.data.get('username') is None:
        raise serializers.ValidationError('User does not exist')
    user_instance = get_object_or_404(
        User, username=request.data.get('username')
    )
    serializer = TokenSerializer(user_instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class CategoryViewSet(CreateListDestroyViewset):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewset):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_classes = {
        'list': TitleReadSerializer,
        'create': TitleWriteSerializer,
        'retrieve': TitleReadSerializer,
        'update': TitleWriteSerializer,
        'partial_update': TitleWriteSerializer,
        'destroy': TitleWriteSerializer
    }
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('-name')
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsModerator
                          | IsAdminOrReadOnly | IsSuperuser]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        self.queryset = title.reviews.all()
        return self.queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsModerator
                          | IsAdminOrReadOnly | IsSuperuser]

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.get_review())

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review_id=self.get_review())
