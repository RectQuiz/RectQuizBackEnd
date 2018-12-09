from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import *


class UserViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TemaViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer

class NivelViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = NivelSerializer

    def get_queryset(self):
        queryset = Nivel.objects.all()
        tema = self.request.query_params.get('tema', None)
        if tema is not None:
            queryset = Nivel.objects.filter(tema=tema)
        return queryset

class QuizViewSet(ModelViewSet):

    serializer_class = QuizSerializer
    def get_queryset(self):
        queryset = Quiz.objects.all()
        nivel = self.request.query_params.get('nivel', None)
        if nivel is not None:
            queryset = Quiz.objects.filter(nivel=nivel)
        return queryset

class DenunciaViewSet(ModelViewSet):

    serializer_class = DenunciaSerializer
    http_method_names = ['post']

    def get_queryset(self):
        query_set = Denuncia.objects.all()
        return query_set

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LocalidadeViewSet(ModelViewSet):

    serializer_class = LocalidadeSerializer

    def get_queryset(self):
        queryset = Localidade.objects.all()
        return queryset
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProgressoTemaViewSet(ModelViewSet):
    serializer_class = ProgressoTemaSerializer

    def get_queryset(self):
        queryset = ProgressoTema.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProgressoNivelViewSet(ModelViewSet):
    serializer_class = ProgressoNivelSerializer

    def get_queryset(self):
        queryset = ProgressoNivel.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProgressoQuizViewSet(ModelViewSet):
    serializer_class = ProgressoQuizSerializer

    def get_queryset(self):
        queryset = ProgressoQuiz.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RespostaQuizViewSet(ModelViewSet):
    serializer_class = RespostaQuizSerializer

    def get_queryset(self):
        queryset = RespostasQuiz.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





