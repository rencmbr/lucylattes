# CALCULA OS INDICADORES USADOS NO PPGEE COM A FINALIDADE DE CREDENCIAMENTO
#
# Adaptado por Renato Cardoso Mesquita para o PPGEE-Lucy
# a partir do trabalho de Alessandro Beda, que escreveu as rotinas originais em MATLAB

import pandas as pd
import os
import glob
from collections import OrderedDict
from datetime import datetime
import ppgee_resources.authorsclassification as ac
from resources.support_functions import yearlimit_forfilter

def extrai_ano_data_string_sem_barras(data_str):
        if data_str != '':
            return datetime.strptime(data_str, '%d%m%Y').year
        else:
            return 0

def get_artigos_faixa_anos_com_duplicados(id_docentes_a_remover):
    #=========================================================
    # Busca todos os artigos publicados na faixa de anos especificada
    # no arquivo de configuração de entrada (config_tk.txt)
    # artigos publicados por mais de um docente aparecerão em duplicata
    #=========================================================
    df=pd.read_csv('./csv_producao/papers_all.csv', 
                        header=0, dtype=str, encoding='ISO-8859-1')
    
    # Remove os artigos dos docentes na lista de ids a remover
    df = df.drop(df[df['ID'].isin(id_docentes_a_remover)].index)

    # Filtra os artigos dos anos da faixa (lida do arquivo config_tk.txt)
    lsyear_limits = yearlimit_forfilter()
    df['YEAR'] = [int(yy) for yy in df['YEAR'].to_list()]
    df = df[(df['YEAR'] >= lsyear_limits[0]) &
                (df['YEAR'] <= lsyear_limits[1])]
    df.reset_index(inplace=True, drop=True)

    # Regulariza os nomes dos autores
    df["AUTHOR"] = df["AUTHOR"].apply(ac.regulariza)
    df["AUTHOR"] = df["AUTHOR"].apply(eval)

    # Remove duplicados da lista de autores
    listaautores = df['AUTHOR'].to_list()
    for i in range(len(listaautores)):
        autoresartigo = listaautores[i]
        listaautores[i] = list(OrderedDict.fromkeys(autoresartigo))
    df["AUTHOR"] = listaautores

    return df

def get_patentes_faixa_anos_com_duplicados(id_docentes_a_remover):
    #=========================================================
    # Busca todas as patentes concedidas na faixa de anos especificada
    # no arquivo de configuração de entrada (config_tk.txt)
    # Patentes com mais de um docente autor aparecerão em duplicata
    #=========================================================
    df=pd.read_csv('./csv_producao/patents_all.csv', 
                        header=0, dtype=str, keep_default_na=False)
    
    # Remove as patentes dos docentes na lista de ids a remover
    df = df.drop(df[df['ID'].isin(id_docentes_a_remover)].index)

    # Filtra as patentes concedidas nos anos da faixa (lida do arquivo config_tk.txt)
    lsyear_limits = yearlimit_forfilter()
    df['YEAR'] = [extrai_ano_data_string_sem_barras(yy) for yy in df['CON_DAY'].to_list()]
    df = df[(df['YEAR'] >= lsyear_limits[0]) &
                (df['YEAR'] <= lsyear_limits[1])]
    df.reset_index(inplace=True, drop=True)

    # Regulariza os nomes dos autores
    df["AUTHOR"] = df["AUTHOR"].apply(ac.regulariza)
    df["AUTHOR"] = df["AUTHOR"].apply(eval)

    # Remove duplicados da lista de autores
    listaautores = df['AUTHOR'].to_list()
    for i in range(len(listaautores)):
        autoresartigo = listaautores[i]
        listaautores[i] = list(OrderedDict.fromkeys(autoresartigo))
    df["AUTHOR"] = listaautores

    return df

def conta_docentes_publicacao(ARTIGO_TABELA_AUTORES,docente_tabela):
    # ====================================================
    # Conta o número de autores que são docentes em cada 
    # publicação (artigo ou patente)
    # ====================================================
    CONTAGEM_DOCENTES = []
    for i in range(len(ARTIGO_TABELA_AUTORES[0])):
        lista_autores_sobrenome = ARTIGO_TABELA_AUTORES[1][i]
        lista_autores_prenome = ARTIGO_TABELA_AUTORES[0][i]
        contagem_docentes = 0
        for j in range(len(lista_autores_sobrenome)):
            find_tipo = False
            if lista_autores_sobrenome[j] in docente_tabela[1]:
                count = docente_tabela[1].count(lista_autores_sobrenome[j])
                k = -1
                for q in range(count):
                    k = docente_tabela[1].index(lista_autores_sobrenome[j],k+1)
                    if lista_autores_prenome[j] == docente_tabela[0][k]:
                        contagem_docentes += 1
                        find_tipo = True
                        break
                    elif lista_autores_prenome[j][0] == docente_tabela[0][k][0] and len(lista_autores_prenome[j])==1:
                        contagem_docentes += 1
                        find_tipo = True
                        break
                    elif lista_autores_prenome[j][0] == docente_tabela[0][k][0] and lista_autores_prenome[j][1] =='.':
                        contagem_docentes += 1
                        find_tipo = True
                        break
        CONTAGEM_DOCENTES.append(contagem_docentes)
    return CONTAGEM_DOCENTES 

def compute_ppq_artigos(artigos_na_faixa_de_anos,df_docentes):
    ppq = []
    qualis_for_ppq = ['A1','A2','A3','A4']
    jcr_for_ppq = 1.5
    for id in df_docentes['ID'].to_list():
        ppq_docente = 0
        resultado = list(artigos_na_faixa_de_anos["ID"] == id) 
        artigos_do_docente = artigos_na_faixa_de_anos.loc[resultado]
        num_docentes_artigo = artigos_na_faixa_de_anos["NUM_DOCENTES"].loc[resultado].to_list()
        jcr_artigo = artigos_na_faixa_de_anos["JCR"].loc[resultado].to_list()
        idx=0
        for qualis in artigos_do_docente['QUALIS'].to_list():
            if qualis in qualis_for_ppq:
                ppq_docente=ppq_docente + 1./num_docentes_artigo[idx]
            elif qualis == 'XX':
                jcr = float(jcr_artigo[idx])
                if jcr >= jcr_for_ppq:
                    ppq_docente = ppq_docente + 1./num_docentes_artigo[idx]    
            idx = idx+1
        ppq.append(ppq_docente)
    return ppq

def compute_ppq_patentes(patentes_na_faixa_de_anos,df_docentes):
    ppq = []
    for id in df_docentes['ID'].to_list():
        ppq_docente = 0
        resultado = list(patentes_na_faixa_de_anos["ID"] == id) 
        patentes_do_docente = patentes_na_faixa_de_anos.loc[resultado]
        num_docentes_patente = patentes_na_faixa_de_anos["NUM_DOCENTES"].loc[resultado].to_list()
        for idx in range(len(patentes_do_docente)):
            ppq_docente=ppq_docente + 1./num_docentes_patente[idx]
        ppq.append(ppq_docente)
    return ppq


def remove_docentes_inferior(df_docentes,id_docentes_remover, ppq_inferior,ja_removidos):
    # Remove os docentes que possuirem ppq <= ppq_inferior
    #
    df_docentes.reset_index(inplace=True, drop=True)
    remover = list(df_docentes['PPQ'] <= ppq_inferior)
    a_remover = df_docentes.loc[remover]
    print("Docentes a remover com ppq_inferior ou igual a ", ppq_inferior)
    print(a_remover)
    remov =pd.concat([a_remover, ja_removidos])
    list_ids = a_remover['ID'].to_list()
    for idx in range(len(list_ids)):
        id_docentes_remover.append(list_ids[idx])
    return id_docentes_remover, remov    

 
def credenciamento_ppgee():
    #===========================================================================
    # Computa os indices para o credenciamento no PPGEE a partir dos dados dos 
    # currículos Lattes
    # 
    ############################################################################
    
    # O processo é iterativo e continua enquanto houver docentes com ppq inferior 
    # ao ppq_limite
    ppq_inferior = 0.
    ppq_limite=2.
    iter = 0
    dir_base = 'ppgee_out/credenciamento/'

    # Remove csv files no diretorio credenciamento.
    fileToRemove = glob.glob(dir_base + '*.xlsx')
    for ff in fileToRemove:
        try:
            os.remove(ff)            
        except OSError as e:
            print("Error: %s : %s" % (ff, e.strerror))

    # Lista com os identificadores Lattes dos docentes a remover nas iterações
    # de cômputo do ppq, até se atingir todos os ppqs maiores que o limiar (limiar=2) 
    id_docentes_remover = [] 
    ja_removidos =  pd.DataFrame()    

    while ppq_inferior < ppq_limite :
        # Lê a tabela dos docentes e os artigos da faixa de anos
        # Elimina das tabelas os docentes cujos identificadores estão em id_docentes_remover
        docentes, df_docentes = ac.tabela_docentes_autores(id_docentes_remover)
        artigos_na_faixa_de_anos = get_artigos_faixa_anos_com_duplicados(id_docentes_remover)

        # Lê a tabela das patentes da faixa de anos
        # Elimina da tabela os docentes cujos identificadores estão em id_docentes_remover
        patentes_na_faixa_de_anos = get_patentes_faixa_anos_com_duplicados(id_docentes_remover)
                
        # Regulariza os dados dos autores dos artigos e patentes para poder classifica-los
        ARTIGO_TABELA_AUTORES = ac.regulariza_autores(artigos_na_faixa_de_anos["AUTHOR"].to_list())
        PATENTE_TABELA_AUTORES = ac.regulariza_autores(patentes_na_faixa_de_anos["AUTHOR"].to_list())

        # Conta o número de docentes autores por artigo e por patente - adiciona a informaçao
        # nos dataframes de artigos e patentes
        NUMERO_DOCENTES_ARTIGO = conta_docentes_publicacao(ARTIGO_TABELA_AUTORES,docentes)
        NUMERO_DOCENTES_PATENTE = conta_docentes_publicacao(PATENTE_TABELA_AUTORES,docentes)
        artigos_na_faixa_de_anos["NUM_DOCENTES"] = NUMERO_DOCENTES_ARTIGO
        patentes_na_faixa_de_anos["NUM_DOCENTES"] = NUMERO_DOCENTES_PATENTE

        # Calcula os ppqs (de artigos, de patentes e total e adiciona aos dataframes dos docentes)
        ppq_artigos = compute_ppq_artigos(artigos_na_faixa_de_anos, df_docentes)
        ppq_patentes = compute_ppq_patentes(patentes_na_faixa_de_anos, df_docentes)
        ppq = []
        ppq = [ elema + elemp for elema, elemp in zip(ppq_artigos, ppq_patentes)]
        df_docentes["PPQ"] = ppq
        df_docentes["PPQ_ARTIGOS"] = ppq_artigos
        df_docentes["PPQ_PATENTES"] = ppq_patentes

        # Armazena os resultados de cada iteração nos .xlsx de saída
        artigos_na_faixa_de_anos.sort_values(by=["FULL_NAME", "YEAR", "QUALIS"], inplace=True)
        fileartigos = dir_base + 'artigos'+str(iter) + '.xlsx'
        usecols = ['FULL_NAME', 'TITLE','YEAR','DOI', 'JOURNAL', 'ISSN', 'QUALIS', 'JCR', 'NUM_DOCENTES','AUTHOR' ]
        artigos_na_faixa_de_anos.to_excel(fileartigos, columns=usecols)
        df_docentes.sort_values(by="PPQ", inplace=True, ascending=False)
        filedocentes = dir_base + 'docentes'+str(iter) + '.xlsx'
        df_docentes.to_excel(filedocentes)
        patentes_na_faixa_de_anos.sort_values(by=["FULL_NAME", "YEAR"], inplace=True)
        filepatentes = dir_base + 'patentes'+str(iter) + '.xlsx'
        usecols = ['FULL_NAME','TITLE','COUNTRY','YEAR','DEP_DAY','CON_DAY','NUM_DOCENTES','AUTHOR']
        patentes_na_faixa_de_anos.to_excel(filepatentes, columns=usecols)

        # Busca os IDs dos docentes de menor PPQ para serem removidos da proxima iteração
        ppq_inferior = df_docentes['PPQ'].min()
        if ppq_inferior >= ppq_limite:
            break
        id_docentes_remover, ja_removidos = remove_docentes_inferior(df_docentes,id_docentes_remover,
                                                                      ppq_inferior, ja_removidos)
        iter=iter+1
    ja_removidos.sort_values(by="PPQ", inplace=True, ascending=False)
    fileremovidos = dir_base + 'docentes_colaboradores' + '.xlsx'
    ja_removidos.to_excel(fileremovidos)