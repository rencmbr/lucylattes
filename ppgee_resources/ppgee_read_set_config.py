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

