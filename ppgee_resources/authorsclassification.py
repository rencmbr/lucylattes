# CLASSIFICA AUTORES PPGEE
# Adaptado por Renato Cardoso Mesquita para o PPGEE-Lucy
# a partir do trabalho de Ricardo Hiroshi Takahashi 

import re
import pandas as pd
from datetime import datetime
from collections import OrderedDict

def regulariza(texto):
    texto = texto.upper()
    texto = texto.replace('Á','A')
    texto = texto.replace('Ã','A')
    texto = texto.replace('Â','A')
    texto = texto.replace('É','E')
    texto = texto.replace('Ê','E')
    texto = texto.replace('Í','I')
    texto = texto.replace('Ó','O')
    texto = texto.replace('Õ','O')
    texto = texto.replace('Ô','O')
    texto = texto.replace('Ú','U')
    texto = texto.replace('Ç','C')
    texto = texto.replace('Ñ','N')
    texto = texto.replace('.','. ')
    return texto

def extrai_ano_string(data_str):
    return datetime.strptime(data_str, '%d/%m/%y').year

def regulariza_autores(autores):
    tabela_sobrenomes = []
    tabela_prenomes = []
    for lista_nomes in autores:
        Sobrenome = []
        Prenome = []
        for i in range(len(lista_nomes)):
            nomes = lista_nomes[i].split(' ')
            flag_nome = False
            for j in range(len(nomes)):
                if re.search(',',nomes[j]):
                    sobrenome = nomes[j]
                    sobrenome = sobrenome[:len(sobrenome)-1]
                    if len(nomes)>j+1:
                        prenome = nomes[j+1] #[0]
                    else:
                        prenome = 'null'
                    flag_nome = True
                if not flag_nome:
                    sobrenome = nomes[len(nomes)-1]
                    prenome = nomes[0] 
            Prenome.append(prenome)
            Sobrenome.append(sobrenome)
        tabela_sobrenomes.append(Sobrenome)
        tabela_prenomes.append(Prenome)
    return [tabela_prenomes,tabela_sobrenomes]

def regulariza_nomes(lista_nomes):
    Sobrenome = []
    Prenome = []
    for i in range(len(lista_nomes)):
        nomes = lista_nomes[i].split(' ')
        sobrenome = nomes[len(nomes)-1]
        prenome = nomes[0] 
        Prenome.append(prenome)
        Sobrenome.append(sobrenome)
    return [Prenome,Sobrenome]

def tabela_docentes_autores(id_docentes_a_remover):
    # ====================================================
    # Constroi tabela de nomes de docentes do PPGEE
    # ====================================================
    # Busca os dados dos nomes lidos do currículo Lattes
    #
    usecols = ["FULL_NAME", "ID"]
    df = pd.read_csv('./csv_producao/fullname_all.csv', usecols=usecols,
                        header=0, dtype=str, keep_default_na=False)
    
    # Remove os docentes que estão na lista de IDs a remover
    df = df.drop(df[df['ID'].isin(id_docentes_a_remover)].index)
    df.reset_index(inplace=True, drop=True)
    
    df['FULL_NAME']=df['FULL_NAME'].apply(regulariza)
    docente=df["FULL_NAME"].to_list()

    # Busca versões alternativas de nomes no arquivo suplementar de docentes 
    # Por exemplo, docentes com "FILHO" e "JUNIOR" no sobrenome
    filenomesalternativos="ppgee_data/Docentes-PPGEE-NomesAlternativos.csv"
    dfa = pd.read_csv(filenomesalternativos, header=0, dtype=str) 

    for idx in range(len(dfa)):
        nome_entrada = dfa.iloc[idx,0]
        nome = regulariza(nome_entrada)
        docente.append(nome)  
  
    docente_tabela = regulariza_nomes(docente) 
    return docente_tabela, df
    # ====================================================

def tabela_egressos_orientadores(year):
    # ====================================================
    # Constroi tabela de nomes de egressos e orientadores
    # ====================================================
    # Le arquivo com os nomes completos dos egressos e orientadores.
    # Formato do arquivo: arquivo de texto, com os nomes do egresso
    # o nivel (M ou D), o número de matrícula, nome do orientador 
    # e data de defesa.
    # O arquivo tem formato csv (campos separados por virgula) e possui
    # cabeçalhos com os nomes das colunas
    # "FULL_NAME", "NIVEL", "MATRICULA", "ORIENTADOR" e "DEFESA"
    # Caso um egresso tenha mais de uma forma como o nome aparece
    # nas publicacoes, basta incluir na lista as varias formas.
    # OBS: Para um determinado ano, são considerados egressos
    # os que defenderam trabalho até 5 anos antes. Por exemplo,
    # caso o ano seja 2020, buscam-se os dados para os alunos que
    # defenderam de 2015 a 2019 e mais os de 2020.
    
    usecols = ["FULL_NAME", "NIVEL", "ORIENTADOR", "DEFESA"]
    fileegressos="ppgee_data/Egressos-PPGEE-" + year + ".csv"
    df = pd.read_csv(fileegressos, usecols=usecols,
                        header=0, dtype=str, keep_default_na=False)
    ano = int(year)
    lsyear_limits = [ano-5, ano]
   
    df['DEFESA'] = [extrai_ano_string(yy) for yy in df['DEFESA'].to_list()]
    df = df[(df['DEFESA'] >= lsyear_limits[0]) &
                (df['DEFESA'] <= lsyear_limits[1])]
    df.reset_index(inplace=True, drop=True)

    df["FULL_NAME"] = df["FULL_NAME"].apply(regulariza)
    df["ORIENTADOR"] = df["ORIENTADOR"].apply(regulariza)
   
    egresso_tabela = regulariza_nomes(df["FULL_NAME"].to_list())
    orientador_egr_tabela = regulariza_nomes(df["ORIENTADOR"].to_list())

    return egresso_tabela, orientador_egr_tabela, df['NIVEL'].to_list(), df['DEFESA'].to_list()
    # ====================================================

def tabela_discentes_orientadores(year):
    # ====================================================
    # Constroi tabela de nomes de discentes e orientadores
    # ====================================================
    #
    # a partir de arquivo com os nomes completos dos discentes e orientadores
    # Formato do arquivo: arquivo de texto, com os nomes do discente
    # e do orientador separados por ponto-e-virgula e cada par de
    # discente/orientador separado do seguinte por fim-de-linha.
    # Caso um discente tenha mais de uma forma como o nome aparece
    # nas publicacoes, basta incluir na lista as varias formas.
    
    filediscentes = "ppgee_data/Discentes-PPGEE-" + year + ".csv"
    usecols = ["FULL_NAME", "NIVEL", "ORIENTADOR"]
    df = pd.read_csv(filediscentes, usecols=usecols,
                        header=0, dtype=str, keep_default_na=False)

    df["FULL_NAME"] = df["FULL_NAME"].apply(regulariza)
    df["ORIENTADOR"] = df["ORIENTADOR"].apply(regulariza)
   
    discente_tabela = regulariza_nomes(df["FULL_NAME"].to_list())
    orientador_dis_tabela = regulariza_nomes(df["ORIENTADOR"].to_list())
 
    return discente_tabela , orientador_dis_tabela, df['NIVEL'].to_list()
    # ===================================================
def tabela_posdoc(year):
    # ====================================================
    # Constroi tabela de nomes de pos-docs
    # ====================================================
    # Le arquivo com os nomes completos dos posdocs.
    # Formato do arquivo: arquivo de texto, com os nomes do egresso
    # o nivel (P), o número de matrícula, nome do orientador 
    # e data de defesa do doutorado.
    # O arquivo tem formato csv (campos separados por virgula) e possui
    # cabeçalhos com os nomes das colunas
    # "FULL_NAME", "NIVEL", "MATRICULA", "ORIENTADOR" e "DEFESA"
    # Caso um posdoc tenha mais de uma forma como o nome aparece
    # nas publicacoes, basta incluir na lista as varias formas.
    
    usecols = ["FULL_NAME", "NIVEL", "ORIENTADOR", "DEFESA"]
    fileposdoc="ppgee_data/Posdoc-PPGEE-" + year + ".csv"
    df = pd.read_csv(fileposdoc, usecols=usecols,
                        header=0, dtype=str, keep_default_na=False)
    ano = int(year)

    df["FULL_NAME"] = df["FULL_NAME"].apply(regulariza)

    posdoc_tabela = regulariza_nomes(df["FULL_NAME"].to_list())
   
    return posdoc_tabela

def tabela_artigos(year) :
    # ===================================================
    # Gera tabelas de artigos em periodicos para o ano 
    # em análise
    # ===================================================
    # Le os dados que serão usados (todos os artigos, já removidos os duplicados)
    usecols = ["TITLE","YEAR","DOI", "JOURNAL","ISSN","AUTHOR","QUALIS"]
    df = pd.read_csv('./csv_producao/papers_uniq.csv', usecols=usecols,
                        header=0, dtype=str, keep_default_na=False)

    # Filtra os artigos do ano específico 

    resultado = list(df["YEAR"] == year) 
    df = df.loc[resultado]
    df.reset_index(inplace=True, drop=True)

    df["AUTHOR"] = df["AUTHOR"].apply(regulariza)
    df["AUTHOR"] = df["AUTHOR"].apply(eval)

    #Remove autores duplicados na lista de autores
    listaautores = df['AUTHOR'].to_list()
    for i in range(len(listaautores)):
        autoresartigo = listaautores[i]
        listaautores[i] = list(OrderedDict.fromkeys(autoresartigo))
    df["AUTHOR"] = listaautores

    return df
       
def tabela_eventos(year):
    # ===================================================
    # Gera tabelas de producoes em eventos para o ano 
    # em análise
    # ===================================================
    # Le os dados que serão usados (todas as produções, já removidas as duplicatas)
    usecols = ["TITLE","YEAR","AUTHOR"]
    df = pd.read_csv('./csv_producao/worksevents_uniq.csv', usecols=usecols,
                        header=0, dtype=str, keep_default_na=False)
    # Filtra os artigos do ano específico 
 
    resultado = list(df["YEAR"] == year) 
    df = df.loc[resultado]
    df.reset_index(inplace=True, drop=True)

    df["AUTHOR"] = df["AUTHOR"].apply(regulariza)
    df["AUTHOR"] = df["AUTHOR"].apply(eval)

    return df

def identifica_tipo_autores(ARTIGO_TABELA_AUTORES,docente_tabela,
                            egresso_tabela, nivel_egresso, ano_egresso, 
                            posdoc_tabela,discente_tabela, nivel_discente):
    # ====================================================
    # Identifica autores de artigos (em periódicos ou em eventos)
    # ====================================================
    TIPO_AUTOR_ARTIGO = []
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
        
            if not find_tipo:
                if lista_autores_sobrenome[j] in egresso_tabela[1]:
                    count = egresso_tabela[1].count(lista_autores_sobrenome[j])
                    k = -1
                    for q in range(count):
                        k = egresso_tabela[1].index(lista_autores_sobrenome[j],k+1)
                        if lista_autores_prenome[j] == egresso_tabela[0][k]:
                            find_tipo = True
                            tipo.append('egresso('+ nivel_egresso[k] + '-' + str(ano_egresso[k]) + ')')
                            break

                        elif lista_autores_prenome[j][0] == egresso_tabela[0][k][0] and len(lista_autores_prenome[j])==1:
                            find_tipo = True
                            tipo.append('egresso?('+ nivel_egresso[k] + '-' + str(ano_egresso[k]) + ')')
                            break

                        elif lista_autores_prenome[j][0] == egresso_tabela[0][k][0] and lista_autores_prenome[j][1]=='.':
                            find_tipo = True
                            tipo.append('egresso?('+ nivel_egresso[k] + '-' + str(ano_egresso[k]) + ')')
                            break

            if not find_tipo:
                if lista_autores_sobrenome[j] in discente_tabela[1]:
                    count = discente_tabela[1].count(lista_autores_sobrenome[j])
                    k = -1
                    for q in range(count):
                        k = discente_tabela[1].index(lista_autores_sobrenome[j],k+1)
                        if lista_autores_prenome[j] == discente_tabela[0][k]:
                            find_tipo = True
                            tipo.append('discente('+ nivel_discente[k] + ')')
                            break
        
            if not find_tipo:
                if lista_autores_sobrenome[j] in posdoc_tabela[1]:
                    count = posdoc_tabela[1].count(lista_autores_sobrenome[j])
                    k = -1
                    for q in range(count):
                        k = posdoc_tabela[1].index(lista_autores_sobrenome[j],k+1)
                        if lista_autores_prenome[j] == posdoc_tabela[0][k]:
                            find_tipo = True
                            tipo.append('posdoc')
                            break
            
            if not find_tipo:
                tipo.append('externo')
        
        TIPO_AUTOR_ARTIGO.append(tipo)
        CONTAGEM_DOCENTES.append(contagem_docentes)

    return TIPO_AUTOR_ARTIGO 

def insere_classificacao_autores(df,TIPO_AUTOR_ARTIGO):  
    lista_autores = df["AUTHOR"].to_list()
    autores_classificados = []
    for i in range(len(TIPO_AUTOR_ARTIGO)):
        classificados = []
        for j in range(len(TIPO_AUTOR_ARTIGO[i])):
                adiciona = lista_autores[i][j] + ' (' + TIPO_AUTOR_ARTIGO[i][j] + ')'
                classificados.append(adiciona) 
        autores_classificados.append(classificados)
    df["CLASSIFIED_AUTHORS"] = autores_classificados
    return df   



def authors_classification(year):
    #===========================================================================
    #
    # Classifica os autores de artigos e trabalhos em eventos (docentes, discentes
    # egressos, posdoc ou externos)

    # Busca os dados necessários 
    # tabela de docentes - a principio a lista de ids a remover é vazia
    ids_a_remover = []
    docente_tabela, df = tabela_docentes_autores(ids_a_remover)
    # tabela de egressos, seus orientadores e ano de defesa
    egresso_tabela, orientador_egr_tabela, nivel_egresso, ano_egresso = tabela_egressos_orientadores(year)
    # tabela de discentes e seus orientadores
    discente_tabela , orientador_dis_tabela, nivel_discente = tabela_discentes_orientadores(year)
    # tabela de pos_docs
    posdoc_tabela = tabela_posdoc(year)

    # Dataframes com os dados dos artigos em periódicos e em eventos
    artigos = tabela_artigos(year)
    eventos = tabela_eventos(year) 

    # Regulariza os dados dos autores dos artigos para poder classifica-los
    ARTIGO_TABELA_AUTORES = regulariza_autores(artigos["AUTHOR"].to_list())
    EVENTO_TABELA_AUTORES = regulariza_autores(eventos["AUTHOR"].to_list())

    # Classifica os autores de artigos em periodicos e em eventos
    TIPO_AUTOR_ARTIGO = identifica_tipo_autores(ARTIGO_TABELA_AUTORES,docente_tabela,
                                                egresso_tabela, nivel_egresso, ano_egresso,
                                                posdoc_tabela,
                                                discente_tabela,nivel_discente)
    TIPO_AUTOR_EVENTO = identifica_tipo_autores(EVENTO_TABELA_AUTORES,docente_tabela,
                                                egresso_tabela, nivel_egresso, ano_egresso,
                                                posdoc_tabela,
                                                discente_tabela, nivel_discente)
    
    # Insere a classificação dos autores nos dataframes de artigos em periodicos e eventos

    artigos_com_autores_classificados = insere_classificacao_autores(artigos,TIPO_AUTOR_ARTIGO)
    eventos_com_autores_classificados = insere_classificacao_autores(eventos,TIPO_AUTOR_EVENTO)

    # Gera os artigos (.csv) com os dados dos artigos e classificação dos autores

    out_path = 'ppgee_out/classificaautores/'
    
    columns = ["TITLE","YEAR","DOI", "JOURNAL","ISSN","QUALIS","CLASSIFIED_AUTHORS"]
    file_saida_artigos = out_path + 'artigosclassificados-PPGEE-' + year + '.csv'
    artigos_com_autores_classificados.to_csv(file_saida_artigos, columns=columns)
    print('- O arquivo com a classificação dos autores de artigos foi gerado em ', file_saida_artigos)

    columns = ["TITLE","YEAR","CLASSIFIED_AUTHORS"]
    file_saida_eventos = out_path + 'eventosclassificados-PPGEE-' + year + '.csv'
    eventos_com_autores_classificados.to_csv(file_saida_eventos, columns=columns)
    print('- O arquivo com a classificação dos autores de publicações em eventos foi gerado em ', file_saida_eventos)
