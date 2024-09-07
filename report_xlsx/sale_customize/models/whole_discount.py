""" Initialize Whole Discount """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models, Command
from odoo.exceptions import UserError, ValidationError, Warning


class WholeDiscount(models.Model):
    """
        Initialize Whole Discount:
         -
    """
    _name = 'whole.discount'
    _description = 'Whole Discount'

    name = fields.Char(
        required=True,
        translate=True,
    )
    partner_id = fields.Many2one(
        'res.partner'
    )
    date_from = fields.Date()
    date_to = fields.Date()
    type = fields.Selection(
        [('both', 'Both'),
         ('first', 'First'),
         ('second', 'Second')],
        default='both',
    )
    type_1 = fields.Selection(
        [('first', 'All Amount'),
         ('second', 'After Odoo Discount')],
        default='second',
        string='First Whole Discount Type'
    )
    type_2 = fields.Selection(
        [('first', 'All Amount'),
         ('second', 'After Odoo Discount'),
         ('third', 'After First Discount')],
        default='third',
        string='Second Whole Discount Type'
    )
    first_whole_discount_percentage = fields.Float()
    second_whole_discount_percentage = fields.Float()
    first_whole_discount_amount = fields.Float(
        compute='_compute_first_whole_discount_amount'
    )
    second_whole_discount_amount = fields.Float(
        compute='_compute_first_whole_discount_amount'
    )
    journal_id = fields.Many2one(
        'account.journal'
    )
    whole_discount_line_ids = fields.One2many(
        'whole.discount.line',
        'whole_discount_id'
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done')],
        default='draft',
        string='Status'
    )

    @api.depends('whole_discount_line_ids')
    def _compute_first_whole_discount_amount(self):
        """ Compute first_whole_discount_amount value """
        for rec in self:
            if rec.whole_discount_line_ids:
                rec.first_whole_discount_amount = sum(rec.whole_discount_line_ids.mapped('first_discount_amount'))
                rec.second_whole_discount_amount = sum(rec.whole_discount_line_ids.mapped('second_discount_amount'))
            else:
                rec.first_whole_discount_amount = 0
                rec.second_whole_discount_amount = 0

    # def calculate_discount_amount(self):
    #     """ Calculate Discount Amount """
    #     for rec in self:
    #         if rec.type == 'both':
    #             if rec.type_1 == 'first':
    #
    #             rec.first_whole_discount_amount =

    def get_invoices(self):
        """ Get Invoices """
        for rec in self:
            rec.whole_discount_line_ids.unlink()
            if rec.type == 'both':
                invoices = self.env['account.move'].search([
                    ('partner_id', '=', rec.partner_id.id),
                    ('invoice_date', '>=', rec.date_from),
                    ('invoice_date', '<=', rec.date_to),
                    ('move_type', '=', 'out_invoice'),
                    ('first_use', '=', False),
                    ('second_use', '=', False),
                    ('state', '=', 'posted'),
                ])
                if invoices:
                    for inv in invoices:
                        self.env['whole.discount.line'].create({
                            'invoice_id': inv.id,
                            'whole_discount_id': rec.id,
                        })
            elif rec.type == 'first':

                invoices = self.env['account.move'].search([
                    ('partner_id', '=', rec.partner_id.id),
                    ('invoice_date', '>=', rec.partner_id.id),
                    ('invoice_date', '<=', rec.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('first_use', '=', False),
                    ('state', '=', 'posted'),
                ])
                if invoices:
                    for inv in invoices:
                        self.env['whole.discount.line'].create({
                            'invoice_id': inv.id,
                            'whole_discount_id': rec.id,
                        })
            elif rec.type == 'second':
                invoices = self.env['account.move'].search([
                    ('partner_id', '=', rec.partner_id.id),
                    ('invoice_date', '>=', rec.partner_id.id),
                    ('invoice_date', '<=', rec.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('second_use', '=', False),
                    ('state', '=', 'posted'),
                ])
                if invoices:
                    for inv in invoices:
                        self.env['whole.discount.line'].create({
                            'invoice_id': inv.id,
                            'whole_discount_id': rec.id,
                        })

    
    def create_credit_note(self):
        """ Create Credit Note """
        for rec in self:
            line_vals = []
            if rec.first_whole_discount_amount > 0:
                line_vals = [Command.create({
                    'product_id': self.env.company.first_whole_discount_product_id.id or None,
                    'account_id': self.env.company.first_whole_discount_product_id.property_account_income_id.id,
                    'price_unit': rec.first_whole_discount_amount,
                    'quantity': 1,
                })]
            if rec.second_whole_discount_amount > 0:
                line_vals += [Command.create({
                    'product_id': self.env.company.second_whole_discount_product_id.id or None,
                    'account_id': self.env.company.second_whole_discount_product_id.property_account_income_id.id,
                    'price_unit': rec.second_whole_discount_amount,
                    'quantity': 1,
                })]
            if line_vals:
                invoice_create = self.env['account.move'].create({
                    'whole_discount_id': rec.id,
                    'move_type': 'out_refund',
                    'invoice_origin': rec.name,
                    'partner_id': rec.partner_id.id,
                    'invoice_date_due': fields.Date.today(),
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': line_vals,
                })
            for line in rec.whole_discount_line_ids:
                if rec.type == 'both':
                    line.invoice_id.first_use = True
                    line.invoice_id.second_use = True
                elif rec.type == 'first':
                    line.invoice_id.first_use = True
                elif rec.type == 'second':
                    line.invoice_id.second_use = True
            rec.state = 'done'


    def action_view_credit_note(self):
        self.ensure_one()
        form_view_ref = self.env.ref('account.view_move_form', False)
        tree_view_ref = self.env.ref('account.view_move_tree', False)
        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_out_invoice_type')
        result.update({
            'domain': [('whole_discount_id', '=', self.id)],
            'views': [(tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
        })
        return result


class WholeDiscountLine(models.Model):
    """
        Initialize Whole Discount Line:
         -
    """
    _name = 'whole.discount.line'
    _description = 'Whole Discount Line'

    invoice_id = fields.Many2one(
        'account.move'
    )
    whole_discount_id = fields.Many2one(
        'whole.discount'
    )
    first_use = fields.Boolean(
        related='invoice_id.first_use'
    )
    second_use = fields.Boolean(
        related='invoice_id.second_use'
    )
    first_discount_amount = fields.Float(
        compute='_compute_first_discount_amount'
    )
    second_discount_amount = fields.Float(
        compute='_compute_second_discount_amount'
    )

    def _compute_first_discount_amount(self):
        """ Compute first_discount_amount value """
        for rec in self:
            if rec.whole_discount_id.type in ['both', 'first']:
                if rec.whole_discount_id.type_1 == 'first':
                    rec.first_discount_amount = rec.whole_discount_id.first_whole_discount_percentage / 100 * rec.invoice_id.all_amount
                    rec.invoice_id.first_discount_amount = rec.first_discount_amount
                elif rec.whole_discount_id.type_1 == 'second':
                    rec.first_discount_amount = rec.whole_discount_id.first_whole_discount_percentage / 100 * rec.invoice_id.amount_total
                    rec.invoice_id.first_discount_amount = rec.first_discount_amount
            else:
                rec.first_discount_amount = 0

    def _compute_second_discount_amount(self):
        """ Compute second_discount_amount value """
        for rec in self:
            if rec.whole_discount_id.type in ['both', 'second']:
                if rec.whole_discount_id.type_2 == 'first':
                    rec.second_discount_amount = rec.whole_discount_id.second_whole_discount_percentage / 100 * rec.invoice_id.all_amount
                elif rec.whole_discount_id.type_2 == 'second':
                    rec.second_discount_amount = rec.whole_discount_id.second_whole_discount_percentage / 100 * rec.invoice_id.amount_total
                elif rec.whole_discount_id.type_2 == 'third':
                    rec.second_discount_amount = rec.whole_discount_id.second_whole_discount_percentage / 100 * (rec.invoice_id.amount_total - rec.invoice_id.first_discount_amount)
            else:
                rec.second_discount_amount = 0