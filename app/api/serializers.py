from django.contrib.auth.hashers import make_password
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer, CharField
from ..models import *


class NivelSerializer(ModelSerializer):
    class Meta:
        model = Nivel
        fields = ('id', 'titulo', 'descricao', 'updated_at', 'tema')
class TemaSerializer(ModelSerializer):
    class Meta:
        model = Tema
        fields = ['id', 'titulo', 'descricao', 'updated_at']

class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'pergunta', 'a', 'b', 'c', 'd', 'resposta', 'explicacao', 'nivel')

class DenunciaSerializer(ModelSerializer):
    class Meta:
        model = Denuncia
        fields = ('id', 'titulo', 'descricao', 'imagem', 'documento', 'latitude', 'longitude')

class UserSerializer(ModelSerializer):
    password = CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

class LocalidadeSerializer(ModelSerializer):

    class Meta:
        model = Localidade
        fields = ('id', 'longitude', 'latitude')

class NivelTotalSerializer(ModelSerializer):
    class Meta:
        model = NivelTotal
        fields = ('id', 'nivel', 'data')

#PROGRESSO
class ProgressoTemaSerializer(ModelSerializer):
    class Meta:
        model = ProgressoTema
        fields = ('id', 'concluido', 'porcentagem', 'tema')

class ProgressoNivelSerializer(ModelSerializer):
    class Meta:
        model = ProgressoNivel
        fields = ('id', 'concluido', 'porcentagem', 'nivel')

class ProgressoQuizSerializer(ModelSerializer):
    class Meta:
        model = ProgressoQuiz
        fields = ('id', 'concluido', 'tempo_resposta', 'quiz')

class RespostaQuizSerializer(ModelSerializer):
    class Meta:
        model = RespostasQuiz
        fields = ('id', 'resposta', 'tempo_resposta', 'quiz')