
{
    'name': 'Product Code',
    'summary': 'Product Code',
    'version': '16.0.0.1.0',
    'category': 'Stock',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/stock_picking.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

