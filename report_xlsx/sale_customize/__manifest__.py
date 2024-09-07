
{
    'name': 'Sale Customize',
    'summary': 'Sale Customize',
    'author': "Mahmoud Elfeky",
    'version': '16.0.0.1.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'sale_margin',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/sale_report_view.xml',
        'views/whole_discount.xml',
        'views/res_config_settings_views.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

