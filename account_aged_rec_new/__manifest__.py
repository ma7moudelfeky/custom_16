# -*- coding: utf-8 -*-
{
    'name': "account_aged_rec_new",

    'summary': """
        Aged Receivable Report""",

    'description': """
        1-Add Invoice Date\n
        2-Aged Receivable fetch data based on invoice date not due date
    """,
    'author': "Awd Soltan",
    'website': "Devsoft",
    'category': 'Accounting',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','account','account_reports'],
    'data': [
        'data/accounts_report_column.xml',
    ],

}