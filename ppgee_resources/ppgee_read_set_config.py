"""Read and generate setup from config txt file."""


class PPGEEconfigSetup:
    """Read config_ppgee.txt file and return an assignment."""

    def __init__(self):
        """Read config_ppgee.txt and return."""
        config_file = open('./config_ppgee.txt', 'r', encoding='UTF-8')
        config_lines = list(config_file.readlines())
        config_file.close()
        self.run_html = config_lines[0].split(':')[1]
        self.run_authorsclassification = config_lines[1].split(':')[1]
        self.classificationyear = config_lines[2].split(':')[1]
        self.run_credenciamento = config_lines[3].split(':')[1]

        self.run_confere_dados = config_lines[4].split(':')[1]
        self.run_bolsas = config_lines[5].split(':')[1]
        

    def run_html_report(self):
        """Return 1 or 0 from config_ppgee.txt to run or not the html report"""
        run_html = self.run_html.rstrip('\n')
        run_html = run_html.strip(' ')
        run_html = int(run_html)
        return run_html

    def run_authors_classification(self):
        """Return 1 or 0 from config_ppgee.txt to run or not the authors classification"""
        run_authorsclassification = self.run_authorsclassification.rstrip('\n')
        run_authorsclassification = run_authorsclassification.strip(' ')
        run_authorsclassification = int(run_authorsclassification)
        return run_authorsclassification

    def classification_year(self):
        """Return the year for the authors classification"""
        classificationyear = self.classificationyear.rstrip('\n')
        classificationyear = classificationyear.strip(' ')
        return classificationyear
    
    def run_credenciamento_ppgee(self):
        """Return 1 or 0 from config_ppgee.txt to run or not the credenciamento docente"""
        run_credenciamento = self.run_credenciamento.rstrip('\n')
        run_credenciamento = run_credenciamento.strip(' ')
        run_credenciamento = int(run_credenciamento)
        return run_credenciamento
    
    def run_confere_dados_ppgee(self):
        """Return 1 or 0 from config_ppgee.txt to run or not the confere credenciamento docente"""
        run_confere_dados = self.run_confere_dados.rstrip('\n')
        run_confere_dados = run_confere_dados.strip(' ')
        run_confere_dados = int(run_confere_dados)
        return run_confere_dados
    
    def run_bolsas_ppgee(self):
        """Return 1 or 0 from config_ppgee.txt to run or not the bolsas_ppgee"""
        run_bolsas = self.run_bolsas.rstrip('\n')
        run_bolsas = run_bolsas.strip(' ')
        run_bolsas = int(run_bolsas)
        return run_bolsas

