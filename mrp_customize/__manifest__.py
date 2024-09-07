
{
    'name': 'Mrp Customize',
    'summary': 'Mrp Customize',
    'author': "Mahmoud Elfeky",
    'version': '16.0.0.1.0',
    'category': 'Manufacture',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/mrp_bom.xml',
        'views/product.xml',
        'views/mrp_production.xml',
        'views/mrp_report.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

