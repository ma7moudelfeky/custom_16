import base64
import io
from openpyxl import Workbook
from odoo import api, models
from io import BytesIO
import xlsxwriter
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError  # Add this line
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas  # Add this import statement


class InvoiceReportWizard(models.TransientModel):
    _name = 'invoice.report.wizard'
    _description = 'Customer Report Wizard'

    due_from = fields.Date(string='Due From', required=True)
    due_to = fields.Date(string='Due To', required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        domain="[('allowed_user_ids', '!=', False)]"
    )
    #
    # @api.depends('due_from', 'due_to')
    # def _compute_duration(self):
    #     for wizard in self:
    #         if wizard.due_from and wizard.due_to:
    #             # No need to convert to datetime.date
    #             # Just use strftime directly on the date objects
    #             due_from_str = wizard.due_from.strftime("%Y-%m-%d")
    #             due_to_str = wizard.due_to.strftime("%Y-%m-%d")
    #
    #             # Calculate the duration in days
    #             duration = (wizard.due_to - wizard.due_from).days
    #             wizard.duration = duration

    @api.constrains('due_from', 'due_to')
    def _check_dates(self):
        for wizard in self:
            if wizard.due_from > wizard.due_to:
                raise models.ValidationError("To date must be greater than or equal to From date!")

    def generate_report_xlsx(self):
        # Create a new workbook and add a worksheet
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Set up styles
        bold = workbook.add_format({'bold': True})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

        # Table 1: Customer Information
        customer_table_headers = ['Customer Name', 'Start Date', 'End Date']
        for col_num, header in enumerate(customer_table_headers):
            worksheet.write(0, col_num, header, bold)

        worksheet.write(1, 0, self.partner_id.name)
        worksheet.write(1, 1, self.due_from, date_format)
        worksheet.write(1, 2, self.due_to, date_format)

        # Table 2: Move Lines
        move_lines_table_headers = ['Date', 'Invoice No', 'Ref', 'Debit', 'Credit', 'Balance']
        for col_num, header in enumerate(move_lines_table_headers):
            worksheet.write(3, col_num, header, bold)

        move_lines = self.env['account.move.line'].search([
            ('move_id.date', '>=', self.due_from),
            ('move_id.date', '<=', self.due_to),
            ('partner_id', '=', self.partner_id.id),
            ("account_id.account_type", "in", ("asset_receivable", "liability_payable")),
            ('move_id.state', '=', 'posted')
        ],
            order='id ASC')

        row = 4
        balance = 0
        for move_line in move_lines:
            balance += move_line.debit
            balance -= move_line.credit
            worksheet.write(row, 0, move_line.move_id.date, date_format)
            worksheet.write(row, 1, move_line.move_id.name)
            worksheet.write(row, 2, move_line.ref)
            worksheet.write(row, 3, move_line.debit)
            worksheet.write(row, 4, move_line.credit)
            worksheet.write(row, 5, balance)
            row += 1

        workbook.close()
        output.seek(0)
        report_data = output.read()

        report_name = "Partner Report"

        # Create a report record and attach the report content
        report = self.env['ir.attachment'].create({
            'name': report_name,
            'datas': base64.b64encode(report_data),
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary'
        })

        # Open the report in a new tab
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{report.id}?download=true',
            'target': 'new',
        }

    def generate_report_pdf(self):
        data = []
        lines = self.env['account.move.line'].search([
            ('move_id.date', '>=', self.due_from),
            ('move_id.date', '<=', self.due_to),
            ("account_id.account_type", "in", ("asset_receivable", "liability_payable")),
            ('partner_id', '=', self.partner_id.id),
            ('move_id.state', '=', 'posted')
        ],
        order='id ASC')
        if lines:
            balance = 0
            for line in lines:
                balance += line.debit
                balance -= line.credit
                date = line.move_id.date
                name = line.move_id.name
                ref = line.name
                duration = 0
                debit = line.debit
                credit = line.credit
                data.append((date, name, ref, duration, debit, credit, balance))

            result = {
                'data': data,
                'due_from': self.due_from,
                'due_to': self.due_to,
                'partner_id': self.partner_id.display_name,
                # 'duration': self.duration,
            }
            return self.env.ref(
                'customer_report.report_invoice_custom').report_action([], data=result)
        else:
            raise ValidationError('There is not data to show !')





