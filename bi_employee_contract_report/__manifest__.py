# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	'name': "Employee Contract Report Odoo App",
	'version': "14.0.0.0",
	'category': "Human Resources",
	'summary': "Print HR contract report for employee print contract report print employee contact report print hr employee contact report print contract report print employee contract report for employee contract pdf report for hr contract pdf report print",
	'description':	"""
                    This odoo app helps user to print employee contract report in PDF file format, User can also print contract report for single or multiple employee at once from "Print" menu under tree or form view.
					""",
	'author': "BrowseInfo",
	"website" : "https://www.browseinfo.in",
	"price": 9,
	"currency": 'EUR',
	'depends': ['base','hr_contract'],
	'data': [
				'report/employee_contract_report.xml',
				'report/employee_contract_report_template.xml',
                'report/employee_contract_report_template1.xml',
			],
	'demo': [],
	'qweb': [],
	'installable': True,
	'auto_install': False,
	'application': False,
	"live_test_url":'https://youtu.be/rkdHXMB2pR4',
	"images":['static/description/Banner.png',
			  'static/description/Firma_Janeth.jpeg'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
