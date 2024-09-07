
{
    'name': 'Invoice Receipt',
    'summary': 'Invoice Receipt',
    'author': "Mahmoud Elfeky",
    'version': '16.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'account',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'report/receipt_template.xml',
        'report/receipt_report.xml',
        # 'wizard/',
        # 'views/',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

