# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    discount_1 = fields.Float()
    discount_2 = fields.Float()
    discount_3 = fields.Float()
    purchase_price = fields.Float(
        'Cost'
    )
    net_price = fields.Float()
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

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["discount_1"] = "l.discount_1"
        res["discount_2"] = "l.discount_2"
        res["discount_3"] = "l.discount_3"
        res["purchase_price"] = "l.purchase_price"
        res["net_price"] = "l.net_price"
        res["type_1"] = "l.type_1"
        res["type_2"] = "l.type_2"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """, l.discount_1"""
        res += """, l.discount_2"""
        res += """, l.discount_3"""
        res += """, l.purchase_price"""
        res += """, l.net_price"""
        res += """, l.type_1"""
        res += """, l.type_2"""
        return res
