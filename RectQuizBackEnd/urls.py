"""RectQuizBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app.api.viewsets import *
from app.models import *
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'denuncias', DenunciaViewSet, basename='Denuncia')
router.register(r'temas', TemaViewSet)
router.register(r'niveis', NivelViewSet, basename='Nivel')
router.register(r'quiz', QuizViewSet, basename='Quiz')
router.register(r'users', UserViewSet)
router.register(r'localidades', LocalidadeViewSet, basename='Localidade')
router.register(r'ptemas', ProgressoTemaViewSet, basename='ProgressoTema')
router.register(r'pniveis', ProgressoNivelViewSet, basename='ProgressoNivel')
router.register(r'pquiz', ProgressoQuizViewSet, basename='ProgressoQuiz')
router.register(r'rquiz', RespostaQuizViewSet, basename='RespostasQuiz')

urlpatterns = [
    path('api/rest/login/', obtain_auth_token),
    path('api/rest/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
