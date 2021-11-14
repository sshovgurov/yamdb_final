from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        if request is not None and request.user and request.user.is_user():
            fields['role'].read_only = True
        return fields


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Invalid username")
        return data


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre
        extra_fields_kwargs = {'slug': {'lookup_field': 'slug'}}


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(required=False, many=True, read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category', 'review')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        allow_null=True,
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Can't be from future!")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = TitleReadSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            user = get_object_or_404(
                User, username=self.context['request'].user
            )
            title = get_object_or_404(
                Title,
                pk=self.context['view'].kwargs.get('title_id')
            )
            if Review.objects.filter(author=user.pk, title=title.pk).exists():
                raise serializers.ValidationError('Обзор уже существует!')
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review_id = ReviewSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
