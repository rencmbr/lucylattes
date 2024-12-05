"""Obtem as informações sobre as patentes a partir dos curriculos lattes xml"""

import glob
import numpy as np
import pandas as pd
from resources.tidydata_csv import concat_df
from resources.tidydata_uniq_titles import drop_similar_rows

def getpatents(zipname, minidomdoc):
    """Get patents from xml file."""

    # get full name 
    id_lattes = str(zipname.split('.')[0])
    full_name = minidomdoc.getElementsByTagName('DADOS-GERAIS')[0] \
        .getAttributeNode('NOME-COMPLETO').nodeValue
    
    # search for producao-tecnica starts here
    chd_prodtecnica = minidomdoc.getElementsByTagName('PRODUCAO-TECNICA')

    if chd_prodtecnica.length > 0:
        chd_patents = chd_prodtecnica[0] \
            .getElementsByTagName('PATENTE')
        len_chd_patents = chd_patents.length

        # Verifica se tem patentes no currículo
        if len_chd_patents > 0:
            ls_pat_title = []
            ls_pat_ano_des = []
            ls_pat_pais = []
            ls_pat_codigo = []
            ls_pat_data_concessao = []
            ls_pat_data_pedido_deposito = []
            ls_pat_instituicao_deposito = []
            ls_pat_nome_depositante = []
            ls_pat_tipo_patente = []
            ls_pat_authors = []

            #Busca os dados de cada patente (somente os que importam para o PPGEE - há muitos outros)
            for idx in range(len_chd_patents):

                title = chd_patents[idx].getElementsByTagName('DADOS-BASICOS-DA-PATENTE')[0] \
                    .getAttributeNode('TITULO').nodeValue
                ano_des = chd_patents[idx].getElementsByTagName('DADOS-BASICOS-DA-PATENTE')[0] \
                    .getAttributeNode('ANO-DESENVOLVIMENTO').nodeValue
                pais = chd_patents[idx].getElementsByTagName('DADOS-BASICOS-DA-PATENTE')[0] \
                    .getAttributeNode('PAIS').nodeValue                
                codigo = chd_patents[idx].getElementsByTagName('DETALHAMENTO-DA-PATENTE')[0] \
                    .getElementsByTagName('REGISTRO-OU-PATENTE')[0] \
                    .getAttributeNode('CODIGO-DO-REGISTRO-OU-PATENTE').nodeValue
                data_concessao = chd_patents[idx].getElementsByTagName('DETALHAMENTO-DA-PATENTE')[0] \
                    .getElementsByTagName('REGISTRO-OU-PATENTE')[0] \
                    .getAttributeNode('DATA-DE-CONCESSAO').nodeValue
                data_pedido_deposito = chd_patents[idx].getElementsByTagName('DETALHAMENTO-DA-PATENTE')[0] \
                    .getElementsByTagName('REGISTRO-OU-PATENTE')[0] \
                    .getAttributeNode('DATA-PEDIDO-DE-DEPOSITO').nodeValue
                instituicao_deposito = chd_patents[idx].getElementsByTagName('DETALHAMENTO-DA-PATENTE')[0] \
                    .getElementsByTagName('REGISTRO-OU-PATENTE')[0] \
                    .getAttributeNode('INSTITUICAO-DEPOSITO-REGISTRO').nodeValue
                nome_depositante = chd_patents[idx].getElementsByTagName('DETALHAMENTO-DA-PATENTE')[0] \
                    .getElementsByTagName('REGISTRO-OU-PATENTE')[0] \
                    .getAttributeNode('NOME-DO-DEPOSITANTE').nodeValue
                tipo_patente = chd_patents[idx].getElementsByTagName('DETALHAMENTO-DA-PATENTE')[0] \
                    .getElementsByTagName('REGISTRO-OU-PATENTE')[0] \
                    .getAttributeNode('TIPO-PATENTE').nodeValue

                # Busca os autores da patente - child producao tecnica -> patentes -> autores
                ls_allauthors = []
                chd_autores = chd_patents[idx].getElementsByTagName('AUTORES')
                len_chd_autores = chd_autores.length

                for idy in range(len_chd_autores):
                    author = chd_autores[idy] \
                        .getAttributeNode('NOME-COMPLETO-DO-AUTOR').nodeValue
                    ls_allauthors.append(author)
                ls_pat_title.append(title)
                ls_pat_ano_des.append(ano_des)
                ls_pat_pais.append(pais) 
                ls_pat_codigo.append(codigo)
                ls_pat_data_pedido_deposito.append(data_pedido_deposito)
                ls_pat_data_concessao.append(data_concessao)
                ls_pat_instituicao_deposito.append(instituicao_deposito)
                ls_pat_nome_depositante.append(nome_depositante)
                ls_pat_tipo_patente.append(tipo_patente)
                ls_pat_authors.append(ls_allauthors)
                
            # write file
            df_patents = pd.DataFrame({'ID': np.repeat(id_lattes,
                                                      len(ls_pat_title)),
                                      'FULL_NAME':np.repeat(full_name,
                                                        len(ls_pat_title)),                
                                      'TITLE': ls_pat_title,
                                      'COUNTRY': ls_pat_pais,
                                      'DEV_YEAR': ls_pat_ano_des,
                                      'CODE': ls_pat_codigo,
                                      'DEP_DAY': ls_pat_data_pedido_deposito,
                                      'CON_DAY': ls_pat_data_concessao,
                                      'INSTI_DEP': ls_pat_instituicao_deposito,
                                      'NAME_DEP': ls_pat_nome_depositante,
                                      'TYPE': ls_pat_tipo_patente,
                                      'AUTHOR': ls_pat_authors
                                      })
            pathfilename = str('./csv_producao/' +
                               id_lattes + '_patents.csv')
            df_patents.to_csv(pathfilename, index=False)
            print('The file ', pathfilename, ' has been writed.')
        else:
            print('The id Lattes ', id_lattes, ' has NO PATENTS.')
    else:
        print('The id Lattes ', id_lattes, ' has NO PRODUCAO-TECNICA.')

def tidydata_patents():
    """Tidy all patents csv files and join them in one csv"""
    # df patents
    lscsv_patents = glob.glob('./csv_producao/*_patents.csv')
    if len(lscsv_patents) == 0:
        print('There is NO xxxxx_patents.csv file')
    else:
        df_patent = pd.DataFrame()
        for idx in range(len(lscsv_patents)):
            df = pd.read_csv(lscsv_patents[idx], header=0, dtype='str')
            df_patent = concat_df(df_patent, df)
        df_patent.reset_index(inplace=True, drop=True)

        # sort by id year
        df_patent.sort_values(by=['ID', 'DEV_YEAR'], inplace=True)
        df_patent.reset_index(inplace=True, drop=True)
        
        # write file
        pathfilename = './csv_producao/patents_all.csv'
        df_patent.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_patent['TITLE']), ' patents')

