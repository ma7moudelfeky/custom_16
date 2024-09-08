
{
    'name': 'Invoice Due Date Activity',
    'version': '16.0.1.0.0',
    'category': 'Sales, Accounting',
    'summary': """Invoice Due Date Activity
    .""",
    'description': """Invoice Due Date Activity
                      .""",
    'depends': ['base', 'account', 'user_notify'],
    'data': [
        'security/security.xml',
        # 'data/mail_data.xml',
        'data/ir_cron_data.xml',
        # 'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
