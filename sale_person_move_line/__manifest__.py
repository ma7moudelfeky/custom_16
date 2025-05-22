

{
    'name': 'Sale Person Move Line',
    'summary': 'Sale Person Move Line',
    'author': "Mahmoud Elfeky",
    'version': '18.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'account',
        'stock',
    ],
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',
        # 'report/',
        #'wizard/',
        'views/account_move.xml',
        'views/stock_move.xml',
        #'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

