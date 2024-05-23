"""Create a dictionary to aid into report setup file."""


def report_setup_dict_base():
    """Return a dictionary."""
    dicreport_setup = dict({
        'advis_all': dict({'pathfilename': './csv_producao/advis_all.csv',
                           'description': 'all advising',
                           'print': 'yes_no',
                           'func': 'column_year'}),
        'advisrunn_all': dict({'pathfilename': './csv_producao/advisrunn_all.csv',
                               'description': 'all running advising',
                               'print': 'yes_no',
                               'func': 'column_year_running'}),
        'books_all': dict({'pathfilename': './csv_producao/books_all.csv',
                           'description': 'all books',
                           'print': 'yes_no',
                           'func': 'column_year'}),
        'books_uniq': dict({'pathfilename': './csv_producao/books_uniq.csv',
                            'description': 'unique books',
                            'print': 'yes_no',
                            'func': 'column_year'}),
        'chapters_all': dict({'pathfilename': './csv_producao/chapters_all.csv',
                              'description': 'all chapters',
                              'print': 'yes_no',
                              'func': 'column_year'}),
        'chapters_uniq': dict({'pathfilename': './csv_producao/chapters_uniq.csv',
                               'description': 'unique chapters',
                               'print': 'yes_no',
                               'func': 'column_year'}),
        'grapho_papernoint': dict({'pathfilename': './csv_producao/papers_withno_interact.csv',
                                   'description': 'file resrchers with no inter',
                                   'print': 'yes_no',
                                   'func': 'column_graphonoint'}),
        'hwebofsci': dict({'pathfilename': './csv_producao_hindex/hindex_websci_papers_tbl.csv',
                           'description': 'hindex from wos for all papers',
                           'print': 'yes_no',
                           'func': 'column_indexh'}),
        'hwebofsci_uniq': dict({'pathfilename': './csv_producao_hindex/hindex_websci_papers_tbl_uniq.csv',
                                'description': 'hindex from wos for unique papers',
                                'print': 'yes_no',
                                'func': 'column_indexh'}),
        'papers_all': dict({'pathfilename': './csv_producao/papers_all.csv',
                            'description': 'all papers',
                            'print': 'yes_no',
                            'func': 'column_year'}),
        'papers_uniq': dict({'pathfilename': './csv_producao/papers_uniq.csv',
                             'description': 'uniq papers',
                             'print': 'yes_no',
                             'func': 'column_year'}),
        'ppe_all': dict({'pathfilename': './csv_producao/ppe_all.csv',
                         'description': 'all research extension projects',
                         'print': 'yes_no',
                         'func': 'column_yearfin'}),
        'ppe_uniq': dict({'pathfilename': './csv_producao/ppe_uniq.csv',
                          'description': 'uniq research extension projects',
                          'print': 'yes_no',
                          'func': 'column_yearfin'}),
        'teaching': dict({'pathfilename': './csv_producao/teaching_all.csv',
                          'description': 'all teaching',
                          'print': 'yes_no',
                          'func': 'column_yearfin'})
    })

    return dicreport_setup
