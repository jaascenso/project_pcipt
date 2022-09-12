from django.contrib import admin
from historia.models import *

class PessoaCitadaAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class CargoTituloAdmin(admin.ModelAdmin):
    list_display = ('id','designacao')

class TemaAdmin(admin.ModelAdmin):
    list_display = ('id','tema_texto')
    
class SubTemaAdmin(admin.ModelAdmin):
    list_display = ('id','subtema_texto')

class TemaSubTemaAdmin(admin.ModelAdmin):
    list_display = ('id',)

class CapitaniaAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class FreguesiaAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class ComarcaAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class TermoAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class RequerenteAdmin(admin.ModelAdmin):
    list_display = ('id','nome','marcador_social','sexo')
    
class DestinatarioAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class SecretarioConselhoAdmin(admin.ModelAdmin):
    list_display = ('id','nome','quem_responde')

class RespostaAdmin(admin.ModelAdmin):
    list_display = ('id','data','ano','resumo','referencia','nova_ordem_n_comprimento','tipologia','registro')
    list_filter = ('tipologia', 'ano')

class ConselheirosAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('id','data_parecer_regio','referencia_documental',\
        'sumula','data_consulta','ano','resumo','parecer_regio','registro')
    list_firter = ('data_consulta','registro')

class UltramarAdmin(admin.ModelAdmin):
    list_display = ('id','resumo','registro','data','referencia','autoridade')

class MandadoAdmin(admin.ModelAdmin):
    list_display = ('id','data','ano','registro','referencia','resumo','mandado','nome_quem_envia')

class ProvocacaoAdmin(admin.ModelAdmin):
    list_display = ('id','resumo','referencia','data','ano',\
        'registro','remetente','destinatario_autoridade')
    list_filter = ('registro','remetente')

admin.site.register(PessoaCitada, PessoaCitadaAdmin)
admin.site.register(CargoTitulo, CargoTituloAdmin)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Subtema, SubTemaAdmin)
admin.site.register(TemaSubtema, TemaSubTemaAdmin) #
admin.site.register(Capitania, CapitaniaAdmin)
admin.site.register(Freguesia, FreguesiaAdmin)
admin.site.register(Comarca, ComarcaAdmin)
admin.site.register(Termo, TermoAdmin)
admin.site.register(Requerente, RequerenteAdmin)
admin.site.register(Destinatario, DestinatarioAdmin)
admin.site.register(SecretarioConselho, SecretarioConselhoAdmin)
admin.site.register(Resposta, RespostaAdmin)
admin.site.register(Conselheiro, ConselheirosAdmin)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Ultramar, UltramarAdmin)
admin.site.register(Mandado,MandadoAdmin)
admin.site.register(Provocacao,ProvocacaoAdmin)