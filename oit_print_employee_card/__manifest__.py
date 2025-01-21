
{
    'name': 'OIT Print Employee Card',
    'summary': 'OIT Print Employee Card',
    'author': "OIT Solutions",
    'company': 'OIT Solutions',
    'website': "http://www.oit-solution.com",
    'version': '16.0.0.1.0',
    'category': "OIT Solutions/apps",
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/hr_employee_badge.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

