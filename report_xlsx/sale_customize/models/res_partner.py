""" Initialize Res Partner """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'

    discount_1 = fields.Float()
    discount_2 = fields.Float()
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
