"""app ppgeelucy"""
import glob
import re
import pandas as pd
import resources
import time
from ppgee_resources.authorsclassification import authors_classification
from ppgee_resources.ppgee_read_set_config import PPGEEconfigSetup
from ppgee_resources.credenciamentoppgee import credenciamento_ppgee


def run_ppgeeLucy():
    "Run ppgeelucy."
    time_initial = time.time()
    configs = resources.configSetup()
    turn_capes_index = configs.run_capes_index()
    turn_hwebsci_index = configs.run_hwebsci_index()
    qf = configs.qualis_file()
    turn_rm_csvfiles = configs.run_rm_csvfiles_infolders()
    resources.remove_csv_producao()

    zipfiles = glob.glob('./xml_zip/*.zip')
    lszip = []
    for idx in range(len(zipfiles)):
        nl = re.findall('[0-9]', zipfiles[idx])
        nl = ''.join(nl) + '.zip'
        lszip.append(nl)

    for zipname in lszip:
        print('---------', zipname, '---------')
        xmlfile = resources.unzip_xml(zipname)
        minidomdoc = resources.getminidom_xmlfile(xmlfile)
        resources.getencoding_minidom(zipname, minidomdoc)
        resources.getgeneraldata(zipname, minidomdoc)
        resources.getgeneraldata_grad(zipname, minidomdoc)
        resources.getgeneraldata_mest(zipname, minidomdoc)
        resources.getgeneraldata_dout(zipname, minidomdoc)
        resources.getresearchextproj(zipname, minidomdoc)
        resources.getworksevents(zipname, minidomdoc)
        resources.getpapers(zipname, minidomdoc, qf)
        resources.getbooks(zipname, minidomdoc)
        resources.getchapters(zipname, minidomdoc)
        resources.getadv(zipname, minidomdoc)
        resources.getadvrunn(zipname, minidomdoc)
        resources.getteaching(zipname, minidomdoc)
        resources.getshortcourse(zipname, minidomdoc)
        resources.getproductsppect(zipname, minidomdoc)
        resources.getproductsppeadv(zipname, minidomdoc)

    resources.tidydata_ppe()
    resources.tidydata_worksevents()
    resources.tidydata_papers()
    resources.tidydata_books()
    resources.tidydata_chapters()
    resources.tidydata_advising()
    resources.tidydata_advisingrunn()
    resources.tidydata_teaching()
    resources.tidydata_fullname()
    resources.tidydata_productsppeadv()
    resources.tidydata_productsppect()
    resources.grapho_paper()

    configsPPGEE=PPGEEconfigSetup()
    turn_html_report = configsPPGEE.run_html_report()
    turn_authors_classification = configsPPGEE.run_authors_classification()
    authors_classification_year = configsPPGEE.classification_year()
    turn_credenciamento = configsPPGEE.run_credenciamento_ppgee()

    
    if turn_hwebsci_index == 1:
        resources.getindex_hwebsci()
    else:
        print('Indicadores Web of Science nao foram gerados.')

    if turn_html_report == 1:
        resources.report_setup_json() 
        resources.report_write(qf)

    if turn_capes_index == 1:
        print('Indicadores capes estao em fase de testes, nao gerados.')
        # capes_indori()
        # capes_indprodart()
        # capes_indautdis()
        # capes_distindproddp()
    else:
        print("Indicadores capes para PPG nao foram gerados.")

    if turn_authors_classification == 1:
        authors_classification(authors_classification_year)

    if turn_credenciamento == 1:
        credenciamento_ppgee()    
    

    if turn_rm_csvfiles == 1:
        resources.remove_csv_producao()
    else:
        print("Arquivos csv mantidos nas pastas.")
    print()

    time_final = time.time()
    total_time = time_final - time_initial
    print('The total time was: {} minutes.'.format(total_time/60))

    # ------------------------------------------------------------
