from urllib import request
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Local, Previsao
from .serializers import LocalSerializer, PrevisaoSerializer
from .armazenaMySQL import ArmazenaMySQL

# Visões
## ViewSets define the view behavior.
# Recupera dados
@api_view(['GET', 'POST'])
def getData_localidades(request):
    try:   
        db = ArmazenaMySQL()
        localidades = db.fetch_localidades()
        if localidades:
            return JsonResponse(localidades, safe=False)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'POST'])
def getData_previsoes(request):
    try:
        db = ArmazenaMySQL()
        previsoes = db.fetch_previsoes()
        if previsoes:
            return JsonResponse(previsoes, safe=False)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Localidades
class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

# Previsoes
class PrevisaoViewSet(viewsets.ModelViewSet):
    queryset = Previsao.objects.all()
    serializer_class = PrevisaoSerializer
