from django.core.management.base import BaseCommand
from django.apps import apps
from historia.models import *
from time import time

import csv, datetime, re

## Separadores usados nos ficheiros
SEPARATOR_1 = chr(29) #GROUP SEPARATOR
SEPARATOR_2 = chr(11) #VERTICAL TAB

## Identificação das colunas nos ficheiros
# # PROVOCACAO
P_RESUMO = 0
P_ID = 1
P_REGISTRO = 2
P_REFERENCIA_DOCUMENTAL = 3
P_DATA = 4
P_ANO = 5
P_REMETENTE = 9
P_TERMO_REMETENTE = 10 #NOME TERMO
P_FICHA_RESPOSTA = 11 ##### MIGRAR #####
P_NOME_REMETENTE = 14 #

# CONSULTA
C_RESUMO = 0
C_ID = 1
C_REGISTRO = 2
C_REFERENCIA_DOCUMENTAL = 3
C_DATA_CONSULTA = 4
C_ANO = 5
C_CONCELHEIRO = 6 # POR MIGRAR
C_DATA_PARECER_REAL = 8
C_PARECER_REGIO = 9
C_SUMULA = 16

# RESPOSTA
R_ID = 0
R_ANO = 1
R_CATEGORIA = 2
R_DATA = 3
R_DATA_PROVOCACAO = 4
R_DESTINATARIO = 5
R_DIPLOMATICA = 6
R_FKPETICAO = 8 ##### MIGRAR #####
R_IDENTIFICACAO = 9
R_PROC_REGIOS = 16
R_REFERENCIA = 17
R_REGISTRO = 18
R_REMETENTE = 19
R_RESUMO = 20
R_TERMO_REMETENTE = 21

## Funções auxiliares
def dateFromString(data):
    aux_data = data.split('/')
    try: 
        return datetime.datetime(
            year=int(aux_data[2]),
            month=int(aux_data[1]),
            day=int(aux_data[0])
            )
    except:
        print(data, aux_data)
        return None

## Funções de Migração
# MIGRACAO - FASE 1 - Ficheiro Provocacao
def migracao_provocacao(ficheiro_provocacao):

    print('MIGRANDO - FASE 1 - PROVOCACAO')

    f = open(ficheiro_provocacao, encoding="utf8")

    spamreader = csv.reader(f, delimiter=',', quotechar='"')

    count = 0

    for row in spamreader:

        #contador para estatísticas
        count += 1

        ## formatar dados para os objectos
        p_id = int(row[P_ID])
        p_resumo = row[P_RESUMO].strip()
        p_registro = row[P_REGISTRO].strip()
        p_referencia_documental = row[P_REFERENCIA_DOCUMENTAL].strip()
        if len(row[P_DATA].strip()) > 0:
            p_data = dateFromString(row[P_DATA].strip())
        else:
            p_data = None
        
        if len(row[P_DATA].strip()) > 0 and row[P_DATA].strip()[6:10] == row[P_ANO].strip():
            p_ano = row[P_ANO].strip()
        elif not p_data:
            p_ano = row[P_ANO].strip()
        else:
            p_ano = ''
        p_remetente = row[P_REMETENTE].strip()
        t_remetente_nome = row[P_TERMO_REMETENTE].strip()
        a_peticao = [int(fr.strip()) for fr in re.split(';|,', row[P_FICHA_RESPOSTA].replace('*', '')) if fr.strip()]

        #: separar a string pelo caracter SEPARATOR_1 e apenas considerar os que têm tamanho positivo
        #ct_nome_remetente vai receber uma lista de cargos com SEPARATOR_1, vamos iterar essa lista e
        # fazer uma divisão por esses caracteres
        #nome_remetente = [nr for nr in row[P_NOME_REMETENTE].split(SEPARATOR_1) if len(nr) > 0]   VERIFICAR
        #p_nome_remetente_ct = nome_remetente # está a ser colocado na bd a lista com as []        VERIFICAR
        
        ## criar os objectos
        p = Provocacao(
            id = p_id,
            resumo = p_resumo,
            registro = p_registro,
            referencia = p_referencia_documental,
            data = p_data,
            ano = p_ano,
            remetente = p_remetente,
            )

        ## Para testar ##
        # Migrar identificação(antigo) para designação do cargo_titulo do remetente (??) #
        
        nome_remetente = [nr for nr in row[P_NOME_REMETENTE].split(SEPARATOR_1) if len(nr) > 0] 
        for nr_cargo in nome_remetente:
            nr = CargoTitulo.existe(designacao=nr_cargo)
            if not nr:
                nr = CargoTitulo(designacao=nr_cargo)
                nr.save()
            p.cargo_titulo_remetente = nr
        p.save()

        # MIGAR TERMO REMETENTE PARA TERMO_VILA\nome_termo 
        # CONCLUIDO
        nt = Termo.existe(nome=t_remetente_nome)
        if not nt:
            nt = Termo(nome=t_remetente_nome)
            nt.save()
        p.termos.add(nt)

        for p in a_peticao:
            auxTable = AuxProvocacaoResposta(
                peticao=p,
                chave=p_id,
                tipo_chave=AuxProvocacaoResposta.PROVOCACAO
                ).save()
            
    f.close()
    
    return count

# MIGRACAO - FASE 2 - Ficheiro Consulta
def migracao_consulta(ficheiro_consulta):

    print('MIGRANDO - FASE 2 - CONSULTA')

    f = open(ficheiro_consulta, encoding="utf8")

    spamreader = csv.reader(f, delimiter=',', quotechar='"')

    count = 0

    for row in spamreader:

        #contador para estatísticas
        count += 1

        ## formatar dados para os objectos
        c_id = int(row[C_ID])
        if len(row[C_DATA_PARECER_REAL].strip()) > 0:
            c_data_parecer_regio = dateFromString(row[C_DATA_PARECER_REAL].strip())
        else:
            c_data_parecer_regio = None
        c_referencia_documental = row[C_REFERENCIA_DOCUMENTAL].strip()
        c_sumula = row[C_SUMULA].strip()

        if len(row[C_DATA_CONSULTA].strip()) > 0:
            c_data_consulta = dateFromString(row[C_DATA_CONSULTA].strip())
        else:
            c_data_consulta = None
        if len(row[C_DATA_CONSULTA].strip()) > 0 and row[C_DATA_CONSULTA].strip()[6:10] == row[C_ANO].strip():
            c_ano = row[C_ANO].strip()
        elif not c_data_consulta:
            c_ano = row[C_ANO].strip()
        else:
            c_ano = ''
        c_resumo = row[C_RESUMO].strip()
        c_parecer_regio = row[C_PARECER_REGIO].strip()
        c_registro = row[C_REGISTRO].strip()

        ## validacoes

        ## criar os objectos
        c = Consulta(
            id = c_id,
            data_parecer_regio = c_data_parecer_regio,
            referencia_documental = c_referencia_documental,
            sumula = c_sumula,
            data_consulta = c_data_consulta,
            ano = c_ano, 
            resumo = c_resumo,
            parecer_regio = c_parecer_regio,
            registro = c_registro,
            )
        #dest = Destinatario.existe(nome=dest_nome_destinatario)
        #if not dest:
        #    dest = Destinatario(nome=dest_nome_destinatario)
        #    dest.save()
        #c.cargo_titulo_remetente = dest

        #DAQUI
        #: separar a string pelo caracter SEPARATOR_1 e apenas considerar os que têm tamanho positivo
        conselheiros_consulta = [cc for cc in row[C_CONCELHEIRO].split(SEPARATOR_1) if len(cc) > 0]

        #migra concelheiro - sem repetição
        for cc_nome in conselheiros_consulta:
            cc = Conselheiro.existe(nome=cc_nome)
            if not cc:
                cc = Conselheiro(nome=cc_nome)
                cc.save()
            #cn = Conselheiro(nome=cc_nome) #cn - conselheiro nome cn - concelheiro consulta
            #cn.nome = cc
            #cn.save()
            
            c.save()
            c.conselheiros.add(cc)

        #c.conselheiros.add(cc)
        #AQUI

        #c.save()
        
    f.close()

    return count

# MIGRACAO - FASE 3 - Ficheiro Resposta
def migracao_resposta(ficheiro_resposta):

    print('MIGRANDO - FASE 3 - RESPOSTA')
    
    f = open(ficheiro_resposta , mode='r', encoding='utf8')

    spamreader = csv.reader(f, delimiter=',', quotechar='"')

    count = 0

    for row in spamreader:
        
        #contador para estatísticas
        count += 1

        ## formatar dados para os objectos
        r_id = int(row[R_ID])
        if len(row[R_DATA].strip()) > 0:
            r_data = dateFromString(row[R_DATA].strip())
        else:
            r_data = None
        if len(row[R_DATA].strip()) > 0 and row[R_DATA].strip()[6:10] == row[R_ANO].strip():
            r_ano = row[R_ANO].strip()
        elif not r_data:
            r_ano = row[R_ANO].strip()
        else:
            r_ano = ''
        r_resumo = row[R_RESUMO].strip()
        r_referencia = row[R_REFERENCIA].strip()
        r_tipologia = row[R_DIPLOMATICA]
        r_registro = row[R_REGISTRO].strip()
        d_nome = 'não indicado'
        a_peticao = [int(fr.strip()) for fr in re.split(';|,', row[R_FKPETICAO]) if fr.strip()] 

        ## validacoes
        
        ## criar os objectos
        r = Resposta(
            id=r_id, 
            data=r_data,
            ano=r_ano,
            resumo=r_resumo,
            referencia=r_referencia,
            tipologia=r_tipologia,
            registro=r_registro
            )

        r.save()

        #: separar a string pelo caracter SEPARATOR_1 e apenas considerar os que têm tamanho positivo
        cargo_titulos = [ct for ct in row[R_DESTINATARIO].split(SEPARATOR_1) if len(ct) > 0]
        for ct_designacao in cargo_titulos:
            ct = CargoTitulo.existe(designacao=ct_designacao)
            if not ct:
                ct = CargoTitulo(designacao=ct_designacao)
                ct.save()

            d = Destinatario(nome=d_nome)
            d.cargo_titulo = ct
            d.save()

        r.destinatarios.add(d)

        for p in a_peticao:
            auxTable = AuxProvocacaoResposta(
                peticao=p,
                chave=r_id,
                tipo_chave=AuxProvocacaoResposta.RESPOSTA
                ).save()

    f.close()

    return count

# MIGRACAO - FASE 4 - Ligação Provocação/Resposta
def migracao_ligacao():

    print('MIGRANDO - FASE 4 - LIGACAO PROVOCACAO/RESPOSTA')
    
    # Obtem todas as peticoes
    peticoes = AuxProvocacaoResposta.objects.values('peticao').distinct()
    for p in peticoes:
        ligacoes_p = AuxProvocacaoResposta.objects.values('chave').filter(
            peticao=p.get('peticao'),
            tipo_chave=AuxProvocacaoResposta.PROVOCACAO
            )
        ligacoes_r = AuxProvocacaoResposta.objects.values('chave').filter(
            peticao=p.get('peticao'),
            tipo_chave=AuxProvocacaoResposta.RESPOSTA
            )
        if not len(ligacoes_p) == 1: #tem de existir uma provocação (tem que existir uma SÓ provocação para varias respostas)
            print('ERRO - Falta provocação. Existem ' + str(len(ligacoes_p)) + ' provocações e '\
                 + str(len(ligacoes_r)) + ' repostas para a petição ' + str(p.get('peticao')) + '.')
            continue
        # if not len(ligacoes_r) >= 0: # tem que existir pelo menos uma resposta 
        #     print('ERRO - Falta reposta')
        #     continue
        p_id = ligacoes_p[0] # vamos buscar a provocação
        p = Provocacao.existe(id=int(p_id.get('chave'))) # se a provocação existe na base de dados
        if not p:
            print('ERRO - Não existe provocação')
            continue
        for r_id in ligacoes_r: # vamos buscar as respostas desta peticao
            r = Resposta.existe(id=r_id.get('chave')) # se a resposta existe na base de dados
            if not r:
                print('ERRO - Não existe provocação')
                continue
            p.respostas.add(r) # adicionar a resposta à provocação correspondente


## Função Principal - MIGRAÇÃO
def migracao_geral():

    inicial_ts = time()
    
    ultima_migracao = Migracao.objects.order_by('-criado_a')[0]

    stats_provocacao = migracao_provocacao(str(ultima_migracao.ficheiro_provocacao))
    stats_consulta = migracao_consulta(str(ultima_migracao.ficheiro_consulta))
    stats_resposta = migracao_resposta(str(ultima_migracao.ficheiro_resposta))

    migracao_ligacao()
    
    final_ts = time()

    duracao = int(final_ts - inicial_ts)

    stats = {
        'provocacao': stats_provocacao,
        'consulta': stats_consulta,
        'resposta': stats_resposta,
        'duracao': duracao,
    }

    return stats

## Função Principal - APAGAR DADOS EXISTENTES
def apagar_geral():
    historia_models = reversed(list(apps.get_app_config('historia').get_models()))
    for m in historia_models:
        if m != Migracao:
            m.objects.all().delete()
