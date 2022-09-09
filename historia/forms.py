from django import forms
from historia.models import *
from django.utils.translation import gettext_lazy as _

class MigracaoForm(forms.ModelForm):

    apagar_dados = forms.BooleanField(required=False)

    class Meta:
        model = Migracao
        #são usados para gerar o html
        labels = {
              'ficheiro_provocacao': _('Ficheiro PROVOCAÇÃO'),
              'ficheiro_consulta': _('Ficheiro CONSULTA'),
              'ficheiro_resposta': _('Ficheiro RESPOSTA'),
          }
        #identifica os campos do modelo que queremos incluir no form
        fields = ['ficheiro_provocacao', 'ficheiro_consulta', 'ficheiro_resposta']

# class ProvocacaoForm(forms.ModelForm):
#   class Meta:
#     model = Provocacao
#     fields = ['resumo','referencia','data']
