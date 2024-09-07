import base64
import io
from openpyxl import Workbook
from io import BytesIO
import xlsxwriter
from odoo import _, api, fields, models
from odoo.exceptions import UserError  # Add this line
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas  # Add this import statement
class InvoiceReportWizard(models.TransientModel):
    _name = 'invoice.report.wizard'
    _description = 'Invoice Report Wizard'

    due_from = fields.Date(string='Due From', required=True)
    due_to = fields.Date(string='Due To', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    report_format = fields.Selection([('pdf', 'PDF'), ('xlsx', 'XLSX')], string='Report Format', default='pdf', required=True)
    duration = fields.Integer(string='Duration (Days)', compute='_compute_duration', store=True)

    @api.depends('due_from', 'due_to')
    def _compute_duration(self):
        for wizard in self:
            if wizard.due_from and wizard.due_to:
                # No need to convert to datetime.date
                # Just use strftime directly on the date objects
                due_from_str = wizard.due_from.strftime("%Y-%m-%d")
                due_to_str = wizard.due_to.strftime("%Y-%m-%d")

                # Calculate the duration in days
                duration = (wizard.due_to - wizard.due_from).days
                wizard.duration = duration

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
        move_lines_table_headers = ['Date', 'Invoice No', 'Ref', 'duration', 'Debit', 'Credit', 'Balance']
        for col_num, header in enumerate(move_lines_table_headers):
            worksheet.write(3, col_num, header, bold)

        move_lines = self.env['account.move.line'].search([
            ('move_id.date', '>=', self.due_from),
            ('move_id.date', '<=', self.due_to),
            ('partner_id', '=', self.partner_id.id),
            ('move_id.state', '=', 'posted')
        ])

        row = 4
        for move_line in move_lines:
            worksheet.write(row, 0, move_line.move_id.date, date_format)
            worksheet.write(row, 1, move_line.move_id.name)
            worksheet.write(row, 2, move_line.ref)
            worksheet.write(row, 3, move_line.duration)
            worksheet.write(row, 4, move_line.debit)
            worksheet.write(row, 5, move_line.credit)
            worksheet.write(row, 6, move_line.balance)
            row += 1

        workbook.close()
        output.seek(0)
        report_data = output.read()

        report_name = "Invoice_Report.xlsx"

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
        # Create a PDF buffer
        output = BytesIO()

        # Create a PDF document
        pdf = canvas.Canvas(output, pagesize=letter)

        # Set up styles
        pdf.setFont("Helvetica-Bold", 12)

        # Add content to the PDF
        pdf.drawString(100, 800, f"Invoice Report for {self.partner_id.name}")
        pdf.drawString(100, 780, f"Duration: {self.due_from} to {self.due_to}")

        # Draw the first table header
        pdf.drawString(100, 750, "Customer Name")
        pdf.drawString(200, 750, "Start Date")
        pdf.drawString(300, 750, "End Date")

        # Draw move lines (first table)
        row = 730
        pdf.drawString(100, row, str(self.partner_id.name))
        pdf.drawString(200, row, str(self.due_from))
        pdf.drawString(300, row, str(self.due_to))

        # Draw the second table header
        pdf.drawString(100, 700, "Date")
        pdf.drawString(200, 700, "Invoice No")
        pdf.drawString(300, 700, "Ref")
        pdf.drawString(400, 700, "Duration")
        pdf.drawString(500, 700, "Debit")
        pdf.drawString(600, 700, "Credit")
        pdf.drawString(700, 700, "Balance")

        # Draw move lines (second table)
        row = 680
        for move_line in self.env['account.move.line'].search([
            ('move_id.date', '>=', self.due_from),
            ('move_id.date', '<=', self.due_to),
            ('partner_id', '=', self.partner_id.id),
            ('move_id.state', '=', 'posted')
        ]):
            pdf.drawString(100, row, str(move_line.move_id.date))
            pdf.drawString(200, row, str(move_line.move_id.name))
            pdf.drawString(300, row, str(move_line.ref))
            pdf.drawString(400, row, str(move_line.duration))
            pdf.drawString(500, row, str(move_line.debit))
            pdf.drawString(600, row, str(move_line.credit))
            pdf.drawString(700, row, str(move_line.balance))
            row -= 15

        # Save the PDF to the buffer
        pdf.showPage()
        pdf.save()
        output.seek(0)
        pdf_data = output.read()

        # Create a report record and attach the PDF content
        report = self.env['ir.attachment'].create({
            'name': "Invoice_Report.pdf",
            'datas': base64.b64encode(pdf_data),
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




