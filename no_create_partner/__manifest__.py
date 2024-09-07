
{
    'name': 'No Create Partner',
    'summary': 'No Create Partner',
    'author': "Mahmoud Elfeky",
    'version': '16.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'purchase',
        'sale',
        'account',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/account_move.xml',
        'views/account_payment.xml',
        'views/purchase_order.xml',
        'views/sale_order.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

