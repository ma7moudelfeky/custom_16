
{
    'name': 'Irrigation Project Management',
    'summary': 'Irrigation Project Management',
    'author': "Mahmoud Elfeky",
    'version': '16.0.0.1.0',
    'category': 'Project',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'project',
        'hr_timesheet',
        # 'sale_timesheet',
        # 'sale_project',
        'contacts',
        'bi_product_brand',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/project.xml',
        'views/task_quantity_report.xml',
        'views/views.xml',
        'views/project_task.xml',
        'views/portal.xml',
        'data/sequence.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

