
{
    'name': 'invoice  report wizard',
    'summary': '',
    'author': " Mahmoud Elfeky",
    'version': '16.0.0.1.0',
    'category': '',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/invoice_report.xml',
        'wizard/invoice_report_wizard.xml',
        'views/account_move.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

