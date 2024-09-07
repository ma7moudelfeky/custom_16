
{
    'name': 'Invoice Report',
    'summary': 'Invoice Report',
    'version': '16.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'report/account_move_report.xml',
        # 'report/account_move_inh.xml',
        # 'wizard/',
        'views/account_move_report.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

