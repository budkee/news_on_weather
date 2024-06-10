from rest_framework import serializers
from .models import Local, Previsao

# Estado representacional da aplicação
## Serializers define the API representation.
### Porta às localidades
class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'

### Porta às previsões
class PrevisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Previsao
        fields = '__all__'
       