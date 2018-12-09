from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class NivelTotal(models.Model):
    nivel = models.IntegerField(null=False, default=0)
    data = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Localidade(models.Model):
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Denuncia(models.Model):
    TIPOS = (
        ('Em Análise', 'Em Análise'),
        ('Rejeitada', 'Rejeitada'),
        ('Aceita', 'Aceita')
    )
    imagem = models.ImageField("Imagem", upload_to='denuncias/imagens', null=True)
    titulo = models.CharField("Título", max_length=255, null=False)
    descricao = models.TextField("Descrição", null=False)
    verificada = models.CharField(null=False, max_length=19, choices=TIPOS, default="Em Análise")
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    data = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Tema(models.Model):
    titulo = models.CharField("Título", max_length=255, null=False)
    fundo = models.ImageField("Imagem", upload_to='imagens/temas', null=True)
    descricao = models.TextField("Descrição", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ManyToManyField(User, through='ProgressoTema')

    def __str__(self):
        return self.titulo

class Nivel(models.Model):
    titulo = models.CharField("Título", max_length=255, null=False)
    descricao = models.TextField("Descrição", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

    user = models.ManyToManyField(User, through='ProgressoNivel')

    def __str__(self):
        return self.titulo

class Quiz(models.Model):
    pergunta = models.TextField("Pergunta", null=False)
    a = models.CharField("Alternativa A", max_length=255, null=False)
    b = models.CharField("Alternativa B", max_length=255, null=False)
    c = models.CharField("Alternativa C", max_length=255, null=False)
    d = models.CharField("Alternativa D", max_length=255, null=False)
    resposta = models.CharField("Resposta", max_length=255, null=False)
    explicacao = models.TextField("Explicação", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ManyToManyField(User, through='ProgressoQuiz')
    user = models.ManyToManyField(User, through='RespostasQuiz')

    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)

    def __str__(self):
        return self.pergunta

class ProgressoTema(models.Model):
    concluido = models.BooleanField(null=False, default=False)
    porcentagem = models.FloatField('Porcentagem', validators=[MinValueValidator(0), MaxValueValidator(100)],
                                    default=0, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

class ProgressoNivel(models.Model):
    concluido = models.BooleanField(null=False, default=False)
    porcentagem = models.FloatField('Porcentagem', validators=[MinValueValidator(0), MaxValueValidator(100)],
                                    default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)

class ProgressoQuiz(models.Model):
    concluido = models.BooleanField(null=False, default=False)
    tempo_resposta = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class RespostasQuiz(models.Model):
    resposta = models.CharField(max_length=255, null=False)
    tempo_resposta = models.IntegerField(null=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
