# CALCULA OS INDICADORES USADOS NO PPGEE COM A FINALIDADE DE CREDENCIAMENTO
#
# Adaptado por Renato Cardoso Mesquita para o PPGEE-Lucy
# a partir do trabalho de Alessandro Beda, que escreveu as rotinas originais em MATLAB

import pandas as pd
import os
import glob

import ppgee_resources.authorsclassification as ac
from resources.support_functions import yearlimit_forfilter

def get_artigos_faixa_anos_com_duplicados(id_docentes_a_remover):
    #=========================================================
    # Busca todos os artigos publicados na faixa de anos especificada
    # no arquivo de configuração de entrada (config_tk.txt)
    # artigos publicados por mais de um docente aparecerão em duplicata
    #=========================================================
    df=pd.read_csv('./csv_producao/papers_all.csv', 
                        header=0, dtype=str)
    
    # Remove os artigos dos docentes na lista de ids a remover
    df = df.drop(df[df['ID'].isin(id_docentes_a_remover)].index)

    # Filtra os artigos dos anos da faixa (lida do arquivo config_tk.txt)
    lsyear_limits = yearlimit_forfilter()
    df['YEAR'] = [int(yy) for yy in df['YEAR'].to_list()]
    df = df[(df['YEAR'] >= lsyear_limits[0]) &
                (df['YEAR'] <= lsyear_limits[1])]
    df.reset_index(inplace=True, drop=True)

    df["AUTHOR"] = df["AUTHOR"].apply(ac.regulariza)
    df["AUTHOR"] = df["AUTHOR"].apply(eval)

    return df

def conta_docentes_artigo(ARTIGO_TABELA_AUTORES,docente_tabela):
    # ====================================================
    # Conta o número de autores que são docentes em cada artigo
    # ====================================================
    CONTAGEM_DOCENTES = []
    for i in range(len(ARTIGO_TABELA_AUTORES[0])):
        lista_autores_sobrenome = ARTIGO_TABELA_AUTORES[1][i]
        lista_autores_prenome = ARTIGO_TABELA_AUTORES[0][i]
        tipo = []
        contagem_docentes = 0
        for j in range(len(lista_autores_sobrenome)):
            find_tipo = False
            if lista_autores_sobrenome[j] in docente_tabela[1]:
                count = docente_tabela[1].count(lista_autores_sobrenome[j])
                k = -1
                for q in range(count):
                    k = docente_tabela[1].index(lista_autores_sobrenome[j],k+1)
                    if lista_autores_prenome[j] == docente_tabela[0][k]:
                        tipo.append('docente')
                        contagem_docentes += 1
                        find_tipo = True
                        break
                    elif lista_autores_prenome[j][0] == docente_tabela[0][k][0] and len(lista_autores_prenome[j])==1:
                        tipo.append('docente?')
                        contagem_docentes += 1
                        find_tipo = True
                        break
                    elif lista_autores_prenome[j][0] == docente_tabela[0][k][0] and lista_autores_prenome[j][1] =='.':
                        tipo.append('docente?')
                        contagem_docentes += 1
                        find_tipo = True
                        break
        CONTAGEM_DOCENTES.append(contagem_docentes)
    return CONTAGEM_DOCENTES 

def compute_ppq(artigos_na_faixa_de_anos,df_docentes):
    ppq = []
    qualis_for_ppq = ['A1','A2','A3','A4']
    for id in df_docentes['ID'].to_list():
        ppq_docente = 0
        resultado = list(artigos_na_faixa_de_anos["ID"] == id) 
        artigos_do_docente = artigos_na_faixa_de_anos.loc[resultado]
        num_docentes_artigo = artigos_na_faixa_de_anos["NUM_DOCENTES"].loc[resultado].to_list()
        idx=0
        for qualis in artigos_do_docente['QUALIS'].to_list():
            if qualis in qualis_for_ppq:
                ppq_docente=ppq_docente + 1./num_docentes_artigo[idx]
            idx = idx+1
        ppq.append(ppq_docente)
    return ppq

def remove_docentes_inferior(df_docentes,id_docentes_remover, ppq_inferior):
    # Remove os docentes que possuirem ppq <= ppq_inferior
    #
    df_docentes.reset_index(inplace=True, drop=True)
    remover = list(df_docentes['PPQ'] <= ppq_inferior)
    a_remover = df_docentes.loc[remover]
    print("Docentes a remover com ppq_inferior ou igual a ", ppq_inferior)
    print(a_remover)
    list_ids = a_remover['ID'].to_list()
    for idx in range(len(list_ids)):
        id_docentes_remover.append(list_ids[idx])
    return id_docentes_remover    

 
def credenciamento_ppgee():
    #===========================================================================
    # Computa os indices para o credenciamento no PPGEE a partir dos dados dos 
    # currículos Lattes
    # 
    # Lista com os identificadores Lattes dos docentes a remover nas iterações
    # de cômputo do ppq, até se atingir todos os ppqs maiores que o limiar (limiar=2) 
    id_docentes_remover = []

    # Lê a tabela dos docentes e de todos os artigos da faixa de anos
    # Elimina das tabelas os docentes cujos identificadores estão em id_docentes_remover
    # Os artigos são listados mais de uma vez no caso de mais de um docente autor

    # O processo é iterativo e continua enquanto houver docentes com ppq inferior a 2
    ppq_inferior = 0.
    ppq_limite=2.
    iter = 0
    dir_base = 'ppgee_out/credenciamento/'

    # Remove csv file in folder credenciamento.
    fileToRemove = glob.glob(dir_base + '*.csv')
    for ff in fileToRemove:
        try:
            os.remove(ff)            
        except OSError as e:
            print("Error: %s : %s" % (ff, e.strerror))

    while ppq_inferior < ppq_limite :
        docentes, df_docentes = ac.tabela_docentes_autores(id_docentes_remover)
        artigos_na_faixa_de_anos = get_artigos_faixa_anos_com_duplicados(id_docentes_remover)
                
        # Regulariza os dados dos autores dos artigos para poder classifica-los
        ARTIGO_TABELA_AUTORES = ac.regulariza_autores(artigos_na_faixa_de_anos["AUTHOR"].to_list())

        # Conta o número de docentes autores por artigo
        NUMERO_DOCENTES_ARTIGO = conta_docentes_artigo(ARTIGO_TABELA_AUTORES,docentes)
        artigos_na_faixa_de_anos["NUM_DOCENTES"]= NUMERO_DOCENTES_ARTIGO
        fileartigos = dir_base + 'artigos'+str(iter) + '.csv'
        artigos_na_faixa_de_anos.to_csv(fileartigos)
        ppq = compute_ppq(artigos_na_faixa_de_anos,df_docentes)
        df_docentes["PPQ"] = ppq
        df_docentes.sort_values(by="PPQ", inplace=True, ascending=False)
        filedocentes = dir_base + 'docentes'+str(iter) + '.csv'
        df_docentes.to_csv(filedocentes)
        ppq_inferior = df_docentes['PPQ'].min()
        if ppq_inferior >= ppq_limite:
            break
        id_docentes_remover = remove_docentes_inferior(df_docentes,id_docentes_remover, ppq_inferior)
        iter=iter+1