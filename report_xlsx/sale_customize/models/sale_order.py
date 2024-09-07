""" Initialize Model """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrderLine(models.Model):
    """
        Inherit Sale Order Line:
         -
    """
    _inherit = 'sale.order.line'

    all_amount = fields.Float(
        compute='_compute_all_amount'
    )
    discount_1 = fields.Float()
    discount_2 = fields.Float()
    discount_3 = fields.Float()
    type_1 = fields.Selection(
        [('first', 'All Amount'),
         ('second', 'After Odoo Discount')],
        default='second',
    )
    type_2 = fields.Selection(
        [('first', 'All Amount'),
         ('second', 'After Odoo Discount'),
         ('third', 'After First Discount')],
        default='third',
    )
    net_price = fields.Float(
        compute='_compute_net_price',
        store=1
    )

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_discount(self):
        for line in self:
            if not line.product_id or line.display_type:
                line.discount_1 = 0.0

            if not (
                    line.order_id.pricelist_id
                    and line.order_id.pricelist_id.discount_policy == 'without_discount'
            ):
                continue

            line.discount_1 = 0.0

            if not line.pricelist_item_id:
                # No pricelist rule was found for the product
                # therefore, the pricelist didn't apply any discount/change
                # to the existing sales price.
                continue

            line = line.with_company(line.company_id)
            pricelist_price = line._get_pricelist_price()
            base_price = line._get_pricelist_price_before_discount()

            if base_price != 0:  # Avoid division by zero
                discount = (base_price - pricelist_price) / base_price * 100
                if (discount > 0 and base_price > 0) or (discount < 0 and base_price < 0):
                    # only show negative discounts if price is negative
                    # otherwise it's a surcharge which shouldn't be shown to the customer
                    line.discount_1 = discount

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_all_amount(self):
        """ Compute all_amount value """
        for rec in self:
            rec.all_amount = rec.price_unit * rec.product_uom_qty

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id',
                 'discount','discount_2', 'discount_3', 'type_1', 'type_2')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price_subtotal = line.price_unit * line.product_uom_qty
            discount_2_amount = 0
            discount_3_amount = 0
            if line.discount_1:
                price_subtotal = (line.price_unit * line.product_uom_qty) - ((line.price_unit * line.product_uom_qty) * line.discount_1 / 100)
                if line.discount_2 and line.type_1 and line.type_1 == 'first':
                    discount_2_amount = (line.price_unit * line.product_uom_qty) * line.discount_2 / 100
                elif line.discount_2 and line.type_1 and line.type_1 == 'second':
                    discount_2_amount = price_subtotal * line.discount_2 / 100
                second_price_subtotal = price_subtotal - discount_2_amount
                price_subtotal -= discount_2_amount

                if line.discount_3 and line.type_2 and line.type_2 == 'first':
                    discount_3_amount = (line.price_unit * line.product_uom_qty) * line.discount_3 / 100
                elif line.discount_3 and line.type_2 and line.type_2 == 'second':
                    discount_3_amount = second_price_subtotal * line.discount_3 / 100
                elif line.discount_3 and line.type_2 and line.type_2 == 'third':
                    discount_3_amount = price_subtotal * line.discount_3 / 100
                price_subtotal -= discount_3_amount
            amount_untaxed = price_subtotal

            all_amount = line.price_unit * line.product_uom_qty
            discount_amount = all_amount - price_subtotal
            if all_amount > 0:
                line.discount = (discount_amount / all_amount) * 100
            tax_amt = 0
            taxes = line.tax_id.compute_all(
                line.price_unit,
                line.currency_id,
                line.product_uom_qty,
                line.product_id,
                line.order_id.partner_id)["taxes"]
            if taxes:
                for rec in taxes:
                    tax_amt += rec.get("amount")

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': tax_amt,
                'price_total': amount_untaxed + tax_amt,
            })

    @api.depends('price_subtotal', 'product_uom_qty')
    def _compute_net_price(self):
        """ Compute net_price value """
        for rec in self:
            if rec.product_uom_qty:
                rec.net_price = rec.price_subtotal / rec.product_uom_qty
            else:
                rec.net_price = 0

    @api.onchange('product_id')
    def _onchange_product_id_warning(self):
        """ Override _onchange_product_id_warning """
        res = super(SaleOrderLine, self)._onchange_product_id_warning()
        for rec in self:
            if rec.order_id.partner_id:
                rec.discount_2 = rec.order_id.partner_id.discount_1
                rec.discount_3 = rec.order_id.partner_id.discount_2
                rec.type_1 = rec.order_id.partner_id.type_1
                rec.type_2 = rec.order_id.partner_id.type_2
        return res


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed', 'currency_id')
    def _compute_tax_totals(self):
        """ Override _compute_tax_totals """
        res = super(SaleOrder, self)._compute_tax_totals()
        for rec in self:
            rec.tax_totals['amount_untaxed'] = rec.amount_untaxed
            rec.tax_totals['amount_total'] = rec.amount_total
        return res

    def action_confirm(self):
        """ Override action_confirm """
        res = super(SaleOrder, self).action_confirm()
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            raise ValidationError('You must have administrator group !')
        return res