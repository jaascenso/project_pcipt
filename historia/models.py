from django.db import models
from django.utils.translation import gettext_lazy as _

# CONSTANTES #
LENGTH_REGISTRO = 100
LENGTH_REFERENCIA = 500
PATH_UPLOAD = 'historia/dados_upload/'

class PessoaCitada(models.Model):
    nome = models.CharField(max_length=80)
    
    def __str__(self) -> str:
        return self.nome

    #@staticmethod
    #def __str__(self):
    #    return 'id: ' + str(self.id) + 'nome: ' + str(self.nome)

    class Meta:
        verbose_name = _("pessoa citada")
        verbose_name_plural = _("pessoas citadas")

class CargoTitulo(models.Model):
    designacao = models.CharField(max_length=250)
    
    @staticmethod
    def existe(designacao):
        try:
            result = CargoTitulo.objects.get(designacao=designacao)
        except CargoTitulo.DoesNotExist:
            result = None
        return result

    def __str__(self):
        return self.designacao
    
    class Meta:
        verbose_name = _("cargo título")
        verbose_name_plural = _("cargos título")

class Tema(models.Model):
    tema_texto = models.CharField(max_length=50)

    def __str__(self) -> str: 
        return self.tema_texto

class Subtema(models.Model):
    __rn = "subtemas"
    tema = models.ManyToManyField(Tema, through="TemaSubtema", blank=True, related_name=__rn)
    # Atributos da entidade
    subtema_texto = models.CharField(max_length=50)

    def __str__(self) -> str: 
        return self.subtema_texto

class TemaSubtema(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    subtema = models.ForeignKey(Subtema, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("tema e subtema")
        verbose_name_plural = _("temas e subtemas")

class Capitania(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self) -> str: 
        return self.nome

class Freguesia(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self) -> str: 
        return self.nome

class Comarca(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self) -> str: 
        return self.nome

class Termo(models.Model):
    __rn = "termos"
    freguesias = models.ManyToManyField(Freguesia, blank=True, related_name=__rn)
    comarcas = models.ManyToManyField(Comarca, blank=True, related_name=__rn)
    capitania = models.ForeignKey(Capitania, on_delete=models.PROTECT, null=True, blank=True)
    # Atributos da entidade
    nome = models.CharField(max_length=50)

    def __str__(self) -> str: 
        return self.nome

    @staticmethod
    def existe(nome):
        try:
            result = Termo.objects.get(nome=nome)
        except Termo.DoesNotExist:
            result = None
        return result

    def __str__(self):
        return self.nome

class Requerente(models.Model):
    cargo_titulo = models.ForeignKey(CargoTitulo, on_delete=models.PROTECT, null=True, blank=True)
    # Atributos da entidade
    marcador_social = models.CharField(max_length=20)
    MASCULINO = 'M'
    FEMININO = 'F'
    DESCONHECIDO = 'D'
    SEXO_CHOICES = [
        (MASCULINO,'Masculino'),
        (FEMININO,'Feminino'),
        (DESCONHECIDO,'Desconhecido'),
    ]
    sexo = models.CharField(max_length=1, null=True, blank=True, choices=SEXO_CHOICES)
    nome = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.nome
        
class Destinatario(models.Model):
    nome = models.CharField(max_length=60)
    cargo_titulo = models.ForeignKey(CargoTitulo, on_delete=models.PROTECT)

    @staticmethod
    def existe(nome):
        try:
            result = Destinatario.objects.get(nome=nome)
        except Destinatario.DoesNotExist:
            result = None
        return result

    def __str__(self) -> str:
        return self.nome
    
    class Meta:
        verbose_name = _("destinatário")
        verbose_name_plural = _("destinatários")

class SecretarioConselho(models.Model):
    SECRETARIO = 'SECR'
    CONSELHO = 'CONC'
    QUEM_RESPONDE_CHOICES = [
        (SECRETARIO,'Secretário'),
        (CONSELHO,'Conselho')
    ]
    nome = models.CharField(max_length=80)
    quem_responde = models.CharField(max_length=10, choices=QUEM_RESPONDE_CHOICES)

    class Meta:
        verbose_name = _("secretário de concelho")
        verbose_name_plural = _("secretários de concelho")
    
    def __str__(self):
        return self.nome

class Resposta(models.Model):
    __rn = "respostas"
    requerentes = models.ManyToManyField(Requerente, blank=True, related_name=__rn)
    # CONSTRUIR A TABELA requerente_resposta(relação) - nova class - relacionamento ternário
    tema_subtemas = models.ManyToManyField(TemaSubtema, blank=True, related_name=__rn)
    destinatarios = models.ManyToManyField(Destinatario, blank=True, related_name=__rn)
    secretario_concelho = models.ManyToManyField(SecretarioConselho, blank=True, related_name=__rn)
    # Atributos da entidade
    data = models.DateField(null=True, blank=True)
    ano = models.CharField(max_length=4, null=True, blank=True) #
    resumo = models.TextField(null=True, blank=True)
    referencia = models.CharField(max_length=LENGTH_REFERENCIA,null=True, blank=True)
    nova_ordem_n_comprimento = models.CharField(max_length=50, null=True, blank=True)
    INDIRETA = 'Indireta'
    PARTES = 'Partes'
    PROVISOES = 'Provisões'
    OFICIO = 'Ofícios'
    CAPITANIA = 'Capitania'
    ORDEM = 'Ordem'
    ORDINF = 'Ordem de informe'
    PROVISAO = 'Provisão'
    ALVARA = 'Alvará'
    CARTREC = 'Carta de recomendação'
    ORDINF = 'Ordem de informe (com declaração de procedimento)'
    ALVLEI = 'Alvará de Lei'
    LEI = 'Lei'
    MANDATO = 'Mandato'
    ESCUSADA ='Escusada'
    SEMINF = 'Sem informação'
    ORDEM = 'ordem'
    OUTRASCAP ='Outras capitanias'
    TIPOLOGIA_CHOICES = [
        (OUTRASCAP, 'Indireta'),
        (INDIRETA, 'Indireta'),
        (PROVISOES, 'Provisões'),
        (OFICIO, 'Ofício'),
        (CAPITANIA, 'Capitania'),
        (ORDEM,'Ordem'),
        (ORDINF,'Ordem de informe'),
        (PROVISAO,'Provisão'),
        (ALVARA,'Alvará'),
        (CARTREC,'Carta de recomendação'),
        (ORDINF,'Ordem de informe (com declaração de procedimento)'),
        (ALVLEI,'Alvará de Lei'),
        (LEI,'Lei'),
        (MANDATO,'Mandato'),
        (ESCUSADA,'Escusada'),
        (SEMINF,'Sem informação'),
        (ORDEM,'ordem'),
        (OUTRASCAP,'Outras capitanias'),
    ]
    tipologia = models.CharField(max_length=60, choices=TIPOLOGIA_CHOICES, null=True, blank=True)
    PARTES = 'Partes'
    CAPITANIAS = 'Capitania'
    AVULSO = 'Avulso'
    PROVISOES = 'Provisões'
    MINASGERAIS = 'Minas Gerais'
    CAPITANIA = 'Capitanias'
    SERVICOREAL = 'Serviço Real'
    INDIRETA = 'Indireta'
    OUTRASCAPITANIAS = 'Outras Capintanias'
    REGISTRO_CHOICES = [
        (PARTES,'Partes'),
        (CAPITANIAS,'Capitanias'),
        (AVULSO,'Avulso'),
        (MINASGERAIS,'Minas Gerais'),
        (CAPITANIA,'Capitania'),
        (SERVICOREAL,'Serviço Real'),
        (INDIRETA,'Indireta'),
        (OUTRASCAPITANIAS,'Outras Capitanias'),
    ]
    registro = models.CharField(max_length=LENGTH_REGISTRO, choices=REGISTRO_CHOICES, null=True, blank=True)

    @staticmethod
    def existe(id):
        try:
            result = Resposta.objects.get(id=id)
        except Resposta.DoesNotExist:
            result = None
        return result

    def __str__(self):
        return 'Resposta - id: ' + ' | ' + str(self.id) + ' resumo: ' + self.resumo

    def __str__(self):
        return str(self.id)

    
class Conselheiro(models.Model):    
    nome = models.CharField(max_length=80)
    
    #def __str__(self) -> str: 
    #    return self.nome

    @staticmethod
    def existe(nome):
        try:
            result = Conselheiro.objects.get(nome=nome)
        except Conselheiro.DoesNotExist:
            result = None
        return result

    def __str__(self):
        return 'Conselheiro - id: ' + str(self.id) + ' nome: ' + self.nome

class Consulta(models.Model):
    __rn = "consultas"
    respostas = models.ManyToManyField(Resposta, blank=True, related_name=__rn)
    conselheiros = models.ManyToManyField(Conselheiro, blank=True, related_name=__rn)
    requerentes = models.ManyToManyField(Requerente, blank=True, related_name=__rn)
    tema_subtemas = models.ManyToManyField(TemaSubtema, blank=True, related_name=__rn)
    pessoas_citadas = models.ManyToManyField(PessoaCitada, blank=True, related_name=__rn)
    # Atributos da entidade
    data_parecer_regio = models.DateField(null=True, blank=True)
    referencia_documental = models.CharField(max_length=LENGTH_REFERENCIA)
    sumula = models.TextField(null=True, blank=True)
    data_consulta = models.DateField(null=True, blank=True)
    ano = models.CharField(max_length=4, null=True, blank=True)
    resumo = models.TextField(null=True, blank=True)
    parecer_regio = models.TextField(null=True, blank=True)
    MINASGERAIS ='Minas Gerais'
    PARTES = 'Partes'
    CAPITANIAS = 'Capitanias'
    AVULSO = 'Avulso'
    PROVISOES = 'Provisões'
    CAPITANIA = 'Capitania'
    SERVICOREAL = 'Serviço Real'
    INDIRETA = 'Indireta'
    OUTRASCAPITANIAS = 'Outras Capitanias'
    SERVICOREAL = 'Serviço Real'
    REGISTRO_CHOICES = [
        (MINASGERAIS,'Minas Gerais'),
        (PARTES,'Partes'),
        (CAPITANIAS,'Capitanias'),
        (AVULSO,'Avulso'),
        (MINASGERAIS,'Minas Gerais'),
        (CAPITANIA,'Capitania'),
        (SERVICOREAL,'Serviço Real'),
        (INDIRETA,'Indireta'),
        (SERVICOREAL,'Serviço Real'),
        (OUTRASCAPITANIAS,'Outras Capitanias'),
    ]
    registro = models.CharField(
        max_length=LENGTH_REGISTRO,
        choices=REGISTRO_CHOICES
    )

    def __str__(self):
        return str(self.id)

class Ultramar(models.Model):
    __rn = "ultramares"
    tema_subtemas = models.ManyToManyField(TemaSubtema, blank=True, related_name=__rn)
    respostas = models.ManyToManyField(Resposta, blank=True, related_name=__rn)
    consulta = models.ManyToManyField(Consulta, blank=True, related_name=__rn)
    # Atributos da entidade
    resumo = models.TextField(null=True, blank=True)
    PARTES = 'PART'
    CAPITANIAS = 'CAPIT'
    AVULSO = 'AVUL'
    PROVISOES = 'PROV'
    MINASGERAIS = 'MINASGER'
    CAPITANIA = 'CAPIT'
    SERVICOREAL = 'SERVREAL'
    INDIRETA = 'IND'
    OUTRASCAPITANIAS = 'OUTRASCAPS'
    REGISTRO_CHOICES = [
        (PARTES,'Partes'),
        (CAPITANIAS,'Capitanias'),
        (AVULSO,'Avulso'),
        (MINASGERAIS,'Minas Gerais'),
        (CAPITANIA,'Capitania'),
        (SERVICOREAL,'Serviço Real'),
        (INDIRETA,'Indireta'),
        (OUTRASCAPITANIAS,'Outras Capitanias'),
    ]
    registro = models.CharField(
        max_length=LENGTH_REGISTRO,
        choices=REGISTRO_CHOICES,
    )

    data = models.DateField(null=True, blank=True)
    ano = models.CharField(max_length=4, null=True, blank=True)
    referencia = models.CharField(max_length=LENGTH_REFERENCIA)
    autoridade = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return str(self.id)  

    class Meta:
        verbose_name = _("ultramar")
        verbose_name_plural = _("ultramares")

class Mandado(models.Model):
    __rn = "mandados"
    pessoas_citadas = models.ManyToManyField(PessoaCitada, blank=True, related_name=__rn)
    requerentes = models.ManyToManyField(Requerente, blank=True, related_name=__rn)
    tema_subtemas = models.ManyToManyField(TemaSubtema, blank=True, related_name=__rn)
    respostas = models.ManyToManyField(Resposta, blank=True, related_name=__rn)
    consulta = models.ForeignKey(Consulta, on_delete=models.PROTECT)
    ultramar = models.ForeignKey(Ultramar, on_delete=models.PROTECT)
    # Atributos da entidade
    data = models.DateField(null=True, blank=True)
    ano = models.CharField(max_length=4, null=True, blank=True)
    PARTES = 'PART'
    CAPITANIAS = 'CAPIT'
    AVULSO = 'AVUL'
    PROVISOES = 'PROV'
    MINASGERAIS = 'MINASGER'
    CAPITANIA = 'CAPIT'
    SERVICOREAL = 'SERVREAL'
    INDIRETA = 'IND'
    OUTRASCAPITANIAS = 'OUTRASCAPS'
    REGISTRO_CHOICES = [
        (PARTES,'Partes'),
        (CAPITANIAS,'Capitanias'),
        (AVULSO,'Avulso'),
        (MINASGERAIS,'Minas Gerais'),
        (CAPITANIA,'Capitania'),
        (SERVICOREAL,'Serviço Real'),
        (INDIRETA,'Indireta'),
        (OUTRASCAPITANIAS,'Outras Capitanias'),
    ]
    registro = models.CharField(max_length=LENGTH_REGISTRO, choices=REGISTRO_CHOICES)
    referencia = models.CharField(max_length=LENGTH_REFERENCIA)
    resumo = models.TextField(null=True, blank=True)
    mandado = models.CharField(max_length=80, null=True, blank=True)
    SECRETARIO = 'Secretário'
    CONSELHO = 'Conselho'
    NOME_CHOICES = [
        (SECRETARIO, 'Secretário'),
        (CONSELHO, 'Conselho'),
    ]
    nome_quem_envia = models.CharField(max_length=80, choices=NOME_CHOICES,null=True, blank=True)

    def __str__(self):
        return 'Mandado - id: ' + str(self.id) + ' resumo: ' + self.resumo

class Provocacao(models.Model):
    __rn = "provocacoes"
    ultramar = models.ManyToManyField(Ultramar, blank=True, related_name=__rn)
    mandado = models.ManyToManyField(Mandado, blank=True, related_name=__rn)
    consultas = models.ManyToManyField(Consulta, blank=True, related_name=__rn)
    requerentes = models.ManyToManyField(Requerente, blank=True, related_name=__rn,)
    respostas = models.ManyToManyField(Resposta, blank=True, related_name=__rn)
    termos = models.ManyToManyField(Termo, blank=True, related_name=__rn)
    tema_subtemas = models.ManyToManyField(TemaSubtema, blank=True, related_name=__rn)
    pessoas_citadas = models.ManyToManyField(PessoaCitada, blank=True, related_name=__rn)
    cargo_titulo_remetente = models.ForeignKey(CargoTitulo, on_delete=models.PROTECT, null=True, blank=True)
    
    # Atributos da entidade
    resumo = models.TextField(null=True, blank=True)
    referencia = models.CharField(max_length=LENGTH_REFERENCIA)
    data = models.DateField(null=True, blank=True)
    ano = models.CharField(max_length=4, null=True, blank=True)
    registro = models.CharField(max_length=LENGTH_REGISTRO, null=True, blank=True)
    remetente = models.CharField(max_length=150, null=True, blank=True) #Podem estar presentes vários nomes
    destinatario_autoridade = models.CharField(max_length=40,null=True, blank=True) #Confirmar se é campo controlado
    
    @staticmethod
    def existe(id):
        try:
            result = Provocacao.objects.get(id=id)
        except Provocacao.DoesNotExist:
            result = None
        return result

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = _("provocação")
        verbose_name_plural = _("provocações")

class AuxProvocacaoResposta(models.Model):
    PROVOCACAO = 'P'
    RESPOSTA = 'R'
    TIPO_CHAVE_CHOICES = [
        (PROVOCACAO, 'Provocação'),
        (RESPOSTA, 'Resposta'),
    ]
    peticao = models.IntegerField()
    chave = models.IntegerField()
    tipo_chave = models.CharField(max_length=1, choices=TIPO_CHAVE_CHOICES)
    

### MIGRACOES
class Migracao(models.Model):
    criado_a = models.DateTimeField(auto_now_add=True)
    ficheiro_provocacao = models.FileField(upload_to=PATH_UPLOAD)
    ficheiro_consulta = models.FileField(upload_to=PATH_UPLOAD)
    ficheiro_resposta = models.FileField(upload_to=PATH_UPLOAD)