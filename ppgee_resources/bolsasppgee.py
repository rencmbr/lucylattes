# CALCULA OS INDICADORES USADOS NO PPGEE COM A FINALIDADE DE ALOCACAO DE BOLSAS
#
# Adaptado por Renato Cardoso Mesquita para o PPGEE-Lucy
# a partir das rotinas de credenciamento docente

import pandas as pd
import os
import glob
from collections import OrderedDict
from datetime import datetime
import ppgee_resources.authorsclassification as ac
import ppgee_resources.credenciamentoppgee as cd 


def compute_pad_artigos(artigos_na_faixa_de_anos,df_docentes):
    pad = []
    qualis_for_pad = ['A1','A2','A3','A4']
    jcr_for_pad = 1.5
    pontuacao_artigo = 50
    for id in df_docentes['ID'].to_list():
        pad_docente = 0
        resultado = list(artigos_na_faixa_de_anos["ID"] == id) 
        artigos_do_docente = artigos_na_faixa_de_anos.loc[resultado]
        jcr_artigo = artigos_na_faixa_de_anos["JCR"].loc[resultado].to_list()
        idx=0
        for qualis in artigos_do_docente['QUALIS'].to_list():
            if qualis in qualis_for_pad:
                pad_docente=pad_docente + pontuacao_artigo
            elif qualis == 'XX':
                jcr = float(jcr_artigo[idx])
                if jcr >= jcr_for_pad:
                    pad_docente = pad_docente + pontuacao_artigo    
            idx = idx+1
        pad.append(pad_docente)
    return pad

def compute_pad_patentes(patentes_na_faixa_de_anos,df_docentes):
    pad = []
    pontuacao_patente=100
    for id in df_docentes['ID'].to_list():
        pad_docente = 0
        resultado = list(patentes_na_faixa_de_anos["ID"] == id) 
        patentes_do_docente = patentes_na_faixa_de_anos.loc[resultado]
        for idx in range(len(patentes_do_docente)):
            pad_docente=pad_docente + pontuacao_patente
        pad.append(pad_docente)
    return pad

def compute_pad_livros(livros_na_faixa_de_anos,df_docentes):
    pad = []
    pontuacao_livro = 100
    for id in df_docentes['ID'].to_list():
        pad_docente = 0
        resultado = list(livros_na_faixa_de_anos["ID"] == id) 
        livros_do_docente = livros_na_faixa_de_anos.loc[resultado]
        for idx in range(len(livros_do_docente)):
            pad_docente=pad_docente + pontuacao_livro
        pad.append(pad_docente)
    return pad

def compute_pad_defesas(year, df_docentes):
    #===============================================================================
    # Computa a parcela dos PADs dos docentes vindas das defesas do ano (year)
    # os dados vem do arquivo Defesas-PPGEE-year.csv (exemplo: Defesas-PPGEE-2024.csv)
    # fornecido pela secretaria do PPGEE
    #
    ################################################################################
    mestrado_valor = 30
    co_mestrado_valor = 15
    doutorado_valor = 100
    co_doutorado_valor = 50
    pad = []

    dirbase = './ppgee_data/'
    filedefesas = dirbase + 'Defesas-PPGEE-' + year + '.csv'
    # Contando as ocorrências
    occurrences = df_docentes['FULL_NAME'].value_counts()  # Contar nomes em df_docentes
    # Criando um DataFrame com os resultados
    result = pd.DataFrame(occurrences).reset_index()
    result.columns = ['FULL_NAME', 'COUNT']

    # Le o arquivo de defesas do ano e regulariza os nomes de orientadores e coorientadores

    df=pd.read_csv(filedefesas, header=0, dtype=str)
    df['ORIENTADOR']=df['ORIENTADOR'].apply(ac.regulariza)
    df['COORIENTADOR 1']=df['COORIENTADOR 1'].apply(ac.regulariza)
    df['COORIENTADOR 2']=df['COORIENTADOR 2'].apply(ac.regulariza)
    df['COORIENTADOR 3']=df['COORIENTADOR 3'].apply(ac.regulariza)

    # Seleciona as defesas de mestrado 
    mestre_df = df[(df['NIVEL'].str.contains('M', na=False)) & 
                   (df['TEXTO FINAL'].str.contains('S', na=False))]
    mestre_df_counts = mestre_df['ORIENTADOR'].value_counts()  # Contar ocorrências mestre_df_counts
    
    # Adicionando contagem de orientacoes de mestrado
    or_mestrado = result['FULL_NAME'].map(mestre_df_counts).fillna(0).astype(int)
    df_docentes['MESTRADO_ORIENTADOR'] = or_mestrado
    
    # Adicionando contagem de coorientacoes de mestrado
    mestre_co1_counts = mestre_df['COORIENTADOR 1'].value_counts() 
    mest_co1 = result['FULL_NAME'].map(mestre_co1_counts).fillna(0).astype(int)
    mestre_co2_counts = mestre_df['COORIENTADOR 2'].value_counts() 
    mest_co2 = result['FULL_NAME'].map(mestre_co2_counts).fillna(0).astype(int)
    mestre_co3_counts = mestre_df['COORIENTADOR 3'].value_counts() 
    mest_co3 = result['FULL_NAME'].map(mestre_co3_counts).fillna(0).astype(int)
    co_mestrado = mest_co1 + mest_co2 + mest_co3
    df_docentes['MESTRADO_COORIENTADOR']= co_mestrado 
    
    # Seleciona as defesas de doutorado
    doutor_df = df[((df['NIVEL'].str.contains('D', na=False)) | 
                    (df['NIVEL'].str.contains('P', na=False))) & 
                   (df['TEXTO FINAL'].str.contains('S', na=False))]
    doutor_df_counts = doutor_df['ORIENTADOR'].value_counts() 
    
    # Adicionando contagem de orientacoes de doutorado
    or_doutorado = result['FULL_NAME'].map(doutor_df_counts).fillna(0).astype(int)
    df_docentes['DOUTORADO_ORIENTADOR'] = or_doutorado
    
    # Adicionando contagem de coorientacoes de doutorado
    doutor_co1_counts = doutor_df['COORIENTADOR 1'].value_counts() 
    doutor_co1 = result['FULL_NAME'].map(doutor_co1_counts).fillna(0).astype(int)
    doutor_co2_counts = doutor_df['COORIENTADOR 2'].value_counts() 
    doutor_co2 = result['FULL_NAME'].map(doutor_co2_counts).fillna(0).astype(int)
    doutor_co3_counts = doutor_df['COORIENTADOR 3'].value_counts() 
    doutor_co3 = result['FULL_NAME'].map(doutor_co3_counts).fillna(0).astype(int)
    co_doutorado = doutor_co1 + doutor_co2 + doutor_co3
    df_docentes['DOUTORADO_COORIENTADOR']= co_doutorado

    # Calcula o delta PAD para as orientações
    for i in range (len(or_mestrado)):
        result = or_mestrado[i] * mestrado_valor + co_mestrado[i] * co_mestrado_valor + \
                 or_doutorado[i] * doutorado_valor + co_doutorado[i] * co_doutorado_valor
        pad.append(result)
          
    return pad, df_docentes



def bolsas_ppgee(year):
    #===========================================================================
    # Computa o delta PAD dos docentes do PPGEE para alocação de bolsas 
    # os dados usados vem dos currículos Lattes e de arquivo com as defesas do ano
    # 
    ############################################################################

    dir_base = 'ppgee_out/pad_bolsas/'
    id_docentes_remover = []    # para computo do delta PAD a lista de docentes a remover é nula
    intyear = int(year)
    lsyear_limits = [intyear,intyear]    # faixa de anos para extrair dados é somente um ano

    # Lê a tabela dos docentes, os artigos, as patentes e os livros na faixa de anos
    docentes, df_docentes = ac.tabela_docentes_autores(id_docentes_remover)
    artigos_na_faixa_de_anos = cd.get_artigos_faixa_anos_com_duplicados(id_docentes_remover,lsyear_limits)
    patentes_na_faixa_de_anos = cd.get_patentes_faixa_anos_com_duplicados(id_docentes_remover,lsyear_limits)
    livros_na_faixa_de_anos = cd.get_livros_faixa_anos_com_duplicados(id_docentes_remover,lsyear_limits)

     # Calcula os pads (de artigos, de patentes,livros, orientações e total) 
     # e adiciona aos dataframes dos docentes)
    pad_artigos = compute_pad_artigos(artigos_na_faixa_de_anos, df_docentes)
    pad_patentes = compute_pad_patentes(patentes_na_faixa_de_anos, df_docentes)
    pad_livros = compute_pad_livros(livros_na_faixa_de_anos, df_docentes)
    pad_defesas, df_docentes = compute_pad_defesas(year, df_docentes)
    pad = []
    pad = [ elema + elemp +eleml + elemd for elema, elemp, eleml, elemd in zip(pad_artigos, pad_patentes, pad_livros, pad_defesas)]
    df_docentes["PAD_DEFESAS"] = pad_defesas
    df_docentes["PAD_ARTIGOS"] = pad_artigos
    df_docentes["PAD_PATENTES"] = pad_patentes
    df_docentes["PAD_LIVROS"] = pad_livros
    df_docentes["PAD_TOTAL"] = pad
    

    # Armazena os resultados no .xlsx de saída
    artigos_na_faixa_de_anos.sort_values(by=["FULL_NAME", "YEAR", "QUALIS"], inplace=True)
    fileartigos = dir_base + 'artigos' + year + '.xlsx'
    usecols = ['FULL_NAME', 'TITLE','YEAR','DOI', 'JOURNAL', 'ISSN', 'QUALIS', 'JCR', 'AUTHOR' ]
    artigos_na_faixa_de_anos.to_excel(fileartigos, columns=usecols)

    df_docentes.sort_values(by="FULL_NAME", inplace=True, ascending=True)
    filedocentes = dir_base + 'PAD_docentes' + year + '.xlsx'
    df_docentes.to_excel(filedocentes)
    
    patentes_na_faixa_de_anos.sort_values(by=["FULL_NAME", "YEAR"], inplace=True)
    filepatentes = dir_base + 'patentes' + year + '.xlsx'
    usecols = ['FULL_NAME','TITLE','COUNTRY','YEAR','DEP_DAY','CON_DAY','AUTHOR']
    patentes_na_faixa_de_anos.to_excel(filepatentes, columns=usecols)

    livros_na_faixa_de_anos.sort_values(by=["TITLE", "YEAR"], inplace=True)
    filelivros = dir_base + 'livros' + year + '.xlsx'
    usecols = ['TITLE','TYPE','YEAR','LANG','PUBLISHER','ISSN','AUTHOR']
    livros_na_faixa_de_anos.to_excel(filelivros, columns=usecols)
