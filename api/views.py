from __future__ import annotations

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .custom_permission import IsAuthorOrAdmin
from .serializers import CommentaireSerializer
from .serializers import CritiqueSerializer
from .serializers import FilmSerializer
from .serializers import InscriptionUserSerializer
from avis.models import Commentaire
from avis.models import Critique
from movie.models import Film


class InscriptionView(CreateAPIView):
    serializer_class = InscriptionUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response(
                {
                    'user': serializer.data,
                    'token': {
                        'access_token': str(access),
                        'refresh_token': str(refresh)
                    }
                },
                status=status.HTTP_201_CREATED
            )


class FilmListCreatView(ListCreateAPIView):
    serializer_class = FilmSerializer
    queryset = Film.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return super().create(request, *args, **kwargs)


class FilmDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FilmSerializer
    queryset = Film.objects.all()
    lookup_field = 'pk'


class CritiqueViewSet(ModelViewSet):
    serializer_class = CritiqueSerializer
    queryset = Critique.objects.all()
    permission_classes = [IsAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        update_at = timezone.now()


class CommentaireViewSet(ModelViewSet):
    serializer_class = CommentaireSerializer
    permission_classes = [IsAuthorOrAdmin]
    queryset = Commentaire.objects.all()

    def perform_create(self, serializer):
        critique = self.request.data.get('critique')
        serializer.save(user=self.request.user, critique_id=critique)
        serializer.save()
