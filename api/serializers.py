from __future__ import annotations

from rest_framework import serializers

from account.models import User
from avis.models import Commentaire
from avis.models import Critique
from avis.models import LikeDislike
from movie.models import Film


class InscriptionUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        max_length=30, label="Mot de pass", required=True, write_only=True)
    password2 = serializers.CharField(
        max_length=30, label="Confirmation", required=True, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'profil', 'role', 'password1', 'password2',)

    def validate(self, data):
        if data['password1'] != data['password2']:
            return serializers.ValidationError('les mots de passes sont different')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class FilmSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Film
        fields = '__all__'
        read_only_fields = ('accept_admin', 'uid', 'user',)


class CritiqueSerializer(serializers.HyperlinkedModelSerializer):
    film = serializers.HyperlinkedRelatedField(
        view_name='film_update_retrieve_destory', queryset=Film.objects.all())
    username = serializers.SerializerMethodField()

    class Meta:
        model = Critique
        fields = ('url', 'pk', 'film', 'username',
                  'title', 'description', 'note',)
        read_only_fields = ['pk', 'film', 'username']

    def get_username(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def validate(self, attrs):
        user = self.context['request'].user
        film = attrs.get('film')

        if Film.objects.filter(user=user, film=film):
            return serializers.ValidationError('vous ne pouvez critiquer q\'un seul film ')

        return attrs


class CommentaireSerializer(serializers.ModelSerializer):
    critique = serializers.HyperlinkedRelatedField(
        view_name='critique-detail',
        queryset=Critique.objects.all()
    )
    username = serializers.SerializerMethodField()

    class Meta:
        model = Commentaire
        fields = ('pk', 'comment', 'username', 'critique')
        read_only_fields = ('critique',)

    def get_username(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
