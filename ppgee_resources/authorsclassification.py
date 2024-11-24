# CLASSIFICA AUTORES PPGEE
# Adaptado por Renato Cardoso Mesquita para o PPGEE-Lucy
# a partir do trabalho de Ricardo Hiroshi Takahashi 

import re
import pandas as pd

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
                    prenome = nomes[0] #[0]
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
        # if sobrenome == 'FILHO':
        #     sobrenome = nomes[len(nomes)-2]
        # if sobrenome == 'JUNIOR':
        #     sobrenome = nomes[len(nomes)-2]    
        prenome = nomes[0] #[0]
        Prenome.append(prenome)
        Sobrenome.append(sobrenome)
    return [Prenome,Sobrenome]

def tabela_docentes_autores(year):
    # ====================================================
    # Constroi tabela de nomes de docentes do PPGEE
    # ====================================================
    # Busca os dados dos nomes lidos do currículo Lattes
    #
    usecols = ["FULL_NAME"]
    df = pd.read_csv('./csv_producao/fullname_all.csv', usecols=usecols,
                        header=0, dtype=str)
    docente=[]

    for idx in range(len(df)):
        nome_entrada = df.iloc[idx,0]
        nome = regulariza(nome_entrada)
        docente.append(nome)

    # Busca versões alternativas de nomes no arquivo suplementar de docentes 
    # Por exemplo, docentes com "FILHO" e "JUNIOR" no sobrenome
    filenomesalternativos="ppgee_data/Docentes-PPGEE-NomesAlternativos-" + year + ".csv"
    df = pd.read_csv(filenomesalternativos, header=0, dtype=str) 
    for idx in range(len(df)):
        nome_entrada = df.iloc[idx,0]
        nome = regulariza(nome_entrada)
        docente.append(nome)  
  
    docente_tabela = regulariza_nomes(docente) 
    return docente_tabela
    # ====================================================

def tabela_egressos_orientadores(year):
    # ====================================================
    # Constroi tabela de nomes de egressos e orientadores
    # ====================================================
    # a partir de arquivo com os nomes completos dos egressos e orientadores.
    # Formato do arquivo: arquivo de texto, com os nomes do egresso
    # e do orientador separados por ponto-e-virgula e cada par de
    # egresso/orientador separado do seguinte por fim-de-linha.
    # OBS: na realidade há campos para mais informações, como CPF, etc.
    # abrir o arquivo csv para ver os demais campos
    # Caso um egresso tenha mais de uma forma como o nome aparece
    # nas publicacoes, basta incluir na lista as varias formas.
    
    fileegressos="ppgee_data/Egressos-PPGEE-" + year + ".csv"
    tabela = []
    filekey = open(fileegressos)
    for linha in filekey:
        linha = linha.rstrip().split(",")
        tabela.append(linha)
    filekey.close()

    egresso = [];
    orientador = [];
    ano = [];
    for entrada in tabela[1:]:
        nome1 = entrada[0]
        nome1 = regulariza(nome1)
        nome2 = entrada[3]
        nome2 = regulariza(nome2)
        data_defesa = entrada[4]
        ano_defesa = int(data_defesa)
        egresso.append(nome1)
        orientador.append(nome2)
        ano.append(ano_defesa)

    egresso_tabela = regulariza_nomes(egresso)
    orientador_egr_tabela = regulariza_nomes(orientador)

    return egresso_tabela, orientador_egr_tabela, ano
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
    tabela = []
    filekey = open(filediscentes)
    for linha in filekey:
        linha = linha.rstrip().split(",")
        tabela.append(linha)
    filekey.close()

    discente = [];
    orient_dis = [];
    for entrada in tabela[1:]:
        nome1 = entrada[0]
        nome1 = regulariza(nome1)
        nome2 = entrada[1]
        nome2 = regulariza(nome2)
        discente.append(nome1)
        orient_dis.append(nome2)

    discente_tabela = regulariza_nomes(discente)
    orientador_dis_tabela = regulariza_nomes(orient_dis)
    return discente_tabela , orientador_dis_tabela
    # ===================================================

def tabela_artigos(year) :
    # ===================================================
    # Gera tabelas de artigos em periodicos para o ano 
    # em análise
    # ===================================================
    # Le os dados que serão usados (todos os artigos)
    usecols = ["TITLE","YEAR","DOI", "JOURNAL","ISSN","AUTHOR","QUALIS"]
    df = pd.read_csv('./csv_producao/papers_all.csv', usecols=usecols,
                        header=0, dtype=str)

    # Filtra os artigos do ano específico 

    resultado = list(df["YEAR"] == year) 
    df = df.loc[resultado]
    df.reset_index(inplace=True, drop=True)

    df["AUTHOR"] = df["AUTHOR"].apply(regulariza)
    df["AUTHOR"] = df["AUTHOR"].apply(eval)

    # ARTIGO_TITULO   = df["TITLE"].to_list()
    # ARTIGO_ANO      = df["YEAR"].to_list()
    # ARTIGO_DOI      = df["DOI"].to_list()
    # ARTIGO_VEICULO  = df["JOURNAL"].to_list()
    # ARTIGO_AUTORES  = df["AUTHOR"].to_list()
    # ARTIGO_QUALIS   = df["QUALIS"].to_list()

    return df
       
def tabela_eventos(year):
    # ===================================================
    # Gera tabelas de producoes em eventos para o ano 
    # em análise
    # ===================================================
    # Le os dados que serão usados (todas as produções)
    usecols = ["TITLE","YEAR","AUTHOR"]
    df = pd.read_csv('./csv_producao/worksevents_all.csv', usecols=usecols,
                        header=0, dtype=str)
    # Filtra os artigos do ano específico 
 
    resultado = list(df["YEAR"] == year) 
    df = df.loc[resultado]
    df.reset_index(inplace=True, drop=True)

    df["AUTHOR"] = df["AUTHOR"].apply(regulariza)
    df["AUTHOR"] = df["AUTHOR"].apply(eval)
 
    # ARTIGO_TITULO   = df["TITLE"].to_list()
    # ARTIGO_ANO      = df["YEAR"].to_list()
    # ARTIGO_DOI      = df["DOI"].to_list()
    # ARTIGO_VEICULO  = df["JOURNAL"].to_list()
    # ARTIGO_AUTORES  = df["AUTHOR"].to_list()
    # ARTIGO_QUALIS   = df["QUALIS"].to_list()
    # EVENTO_TITULO = []
    # EVENTO_ANO = []
    # EVENTO_NOME = []
    # EVENTO_AUTORES = []

    return df

def identifica_tipo_autores(ARTIGO_TABELA_AUTORES,docente_tabela,egresso_tabela,
                       discente_tabela,orientador_egr_tabela,orientador_dis_tabela):
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
                            if orientador_egr_tabela[1][k] in lista_autores_sobrenome:
                                tipo.append('egresso')
                            else:
                                tipo.append('egresso(s/o)')
                            break

                        elif lista_autores_prenome[j][0] == egresso_tabela[0][k][0] and len(lista_autores_prenome[j])==1:
                            find_tipo = True
                            if orientador_egr_tabela[1][k] in lista_autores_sobrenome:
                                tipo.append('egresso?')
                            else:
                                tipo.append('egresso?(s/o)')
                            break

                        elif lista_autores_prenome[j][0] == egresso_tabela[0][k][0] and lista_autores_prenome[j][1]=='.':
                            find_tipo = True
                            if orientador_egr_tabela[1][k] in lista_autores_sobrenome:
                                tipo.append('egresso?')
                            else:
                                tipo.append('egresso?(s/o)')
                            break

            if not find_tipo:
                if lista_autores_sobrenome[j] in discente_tabela[1]:
                    count = discente_tabela[1].count(lista_autores_sobrenome[j])
                    k = -1
                    for q in range(count):
                        k = discente_tabela[1].index(lista_autores_sobrenome[j],k+1)
                        if lista_autores_prenome[j] == discente_tabela[0][k]:
                            find_tipo = True
                            if orientador_dis_tabela[1][k] in lista_autores_sobrenome:
                                tipo.append('discente')
                            else:
                                tipo.append('discente(s/o)')
                            break
            if not find_tipo:
                tipo.append('externo')
        TIPO_AUTOR_ARTIGO.append(tipo)
        CONTAGEM_DOCENTES.append(contagem_docentes)

    return TIPO_AUTOR_ARTIGO 

def insere_classificacao_autores(df,TIPO_AUTOR_ARTIGO):  
    lista_autores = df["AUTHOR"].to_list()
    autores_classificados = []
    for i in range(len(lista_autores)):
        classificados = []
        for j in range(len(lista_autores[i])):
                adiciona = lista_autores[i][j] + ' (' + TIPO_AUTOR_ARTIGO[i][j] + ')'
                classificados.append(adiciona) 
        autores_classificados.append(classificados)
    df["CLASSIFIED_AUTHORS"] = autores_classificados
    return df   



def authors_classification(year):
    #===========================================================================
    #
    # Classifica os autores de artigos e trabalhos em eventos (docentes, discentes
    # egressos ou externos)

    # Busca os dados necessários 
    # tabela de docentes
    docente_tabela = tabela_docentes_autores(year)
    # tabela de egressos, seus orientadores e ano de defesa
    egresso_tabela, orientador_egr_tabela, ano = tabela_egressos_orientadores(year)
    # tabela de discentes e seus orientadores
    discente_tabela , orientador_dis_tabela = tabela_discentes_orientadores(year)

    # Dataframes com os dados dos artigos em periódicos e em eventos
    artigos = tabela_artigos(year)
    eventos = tabela_eventos(year) 

    # Regulariza os dados dos autores dos artigos para poder classifica-los
    ARTIGO_TABELA_AUTORES = regulariza_autores(artigos["AUTHOR"].to_list())
    EVENTO_TABELA_AUTORES = regulariza_autores(eventos["AUTHOR"].to_list())

    # Classifica os autores de artigos em periodicos e em eventos
    TIPO_AUTOR_ARTIGO = identifica_tipo_autores(ARTIGO_TABELA_AUTORES,docente_tabela,
                                                egresso_tabela, discente_tabela,
                                                orientador_egr_tabela,orientador_dis_tabela)
    TIPO_AUTOR_EVENTO = identifica_tipo_autores(EVENTO_TABELA_AUTORES,docente_tabela,
                                                egresso_tabela, discente_tabela,
                                                orientador_egr_tabela,orientador_dis_tabela)
    
    # Insere a classificação dos autores nos dataframes de artigos em periodicos e eventos

    artigos_com_autores_classificados = insere_classificacao_autores(artigos,TIPO_AUTOR_ARTIGO)
    eventos_com_autores_classificados = insere_classificacao_autores(eventos,TIPO_AUTOR_EVENTO)

    # Gera os artigos (.csv) com os dados dos artigos e classificação dos autores

    # TODO: o nome do arquivo poderia ser configurado via arquivo de configuração
    file_saida_artigos = 'ppgee_data/artigosclassificados-PPGEE-' + year + '.csv'
    artigos_com_autores_classificados.to_csv(file_saida_artigos)

    file_saida_eventos = 'ppgee_data/eventosclassificados-PPGEE-' + year + '.csv'
    eventos_com_autores_classificados.to_csv(file_saida_eventos)
