# -*- coding: utf-8 -*-
{
    'name': "custom_vendor_payment",

    'summary': """""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'account_check_printing', 'account', 'mail', 'contacts'],

    'data': [
        # 'security/ir.model.access.csv',
        'security/groups.xml',
        'views/views.xml',
        # 'views/templates.xml',
    ],

    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
