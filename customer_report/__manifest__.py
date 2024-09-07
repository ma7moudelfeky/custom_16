
{
    'name': 'Partner report',
    'version': '16.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account',
        'customer_security',
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/invoice_report.xml',
        'report/account_move_report.xml',
        'wizard/invoice_report_wizard.xml',
        # 'views/account_move.xml',
        # 'views/invoice_report.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

