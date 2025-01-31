
{
    'name': 'HR Employee Incentive Community',
    'summary': 'Employees Incentives | HR Incentives | Incentive | Incentive Advance | HR | HR Bonus | Bonus | Employee Bonus',
    'version': '16.1.0.0.1',
    'description': """
        Helps you to manage Employees Incentives.
        """,
    'category': 'Generic Modules/Human Resources',
    'author': 'Almuoez',
    'depends': [
        'base','hr', 'hr_contract', 'hr_payroll'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/hr_incentive_custom.xml',
        'views/hr_incentive_type.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': '10',
    'currency': 'EUR',
    'license':'OPL-1',
}
