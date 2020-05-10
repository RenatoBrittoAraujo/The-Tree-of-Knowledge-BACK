from rest_framework import serializers
from django.conf import settings
from django.utils.translation import ugettext as _
from .models import User, Contributions
from rest_framework.validators import UniqueValidator

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        label=_("Username"),
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=_('This username is already registered')
            ),
        ],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        label="Email Address",
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        label=_("Password"),
        style={'input_type': 'password'},
        min_length=8,
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def validate_password(self, password):
        min_length = getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
        if len(password) < min_length:
            raise serializers.ValidationError(
                'Password must be at least %s characters' % (min_length)
            )
        return password

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Usuário com este nome já cadastrado'
            )
        return username

    def create(self, validated_data):

        user = User.objects.create_user(
            **validated_data,
        )

        return user

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributions
        fields = ['text']

class UserProfileSerializer(serializers.ModelSerializer):

    contributions = ContributionSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'username',
            'bio',
            'contributionpoints',
            'contributions',
        ]

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'bio'
        ]

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username'
        ]
        read_only = True