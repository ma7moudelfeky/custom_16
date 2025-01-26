

{
    'name': 'Repair Customize',
    'summary': 'Repair Customize',
    'author': "Mahmoud Elfeky",
    'version': '16.0',
    'category': 'Repair',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'repair',
    ],
    'data': [
        'security/security.xml',
        #'security/ir.model.access.csv',
        # 'report/',
        #'wizard/',
        'views/repair_order.xml',
        #'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

