""" Initialize Res Company """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ResCompany(models.Model):
    """
        Inherit Res Company:
         -
    """
    _inherit = 'res.company'

    first_whole_discount_product_id = fields.Many2one(
        'product.product',
        domain="[('detailed_type', '=', 'service')]"
    )
    second_whole_discount_product_id = fields.Many2one(
        'product.product',
        domain="[('detailed_type', '=', 'service')]"
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    first_whole_discount_product_id = fields.Many2one(
        'product.product',
        domain="[('detailed_type', '=', 'service')]",
        related='company_id.first_whole_discount_product_id',
        readonly=0
    )
    second_whole_discount_product_id = fields.Many2one(
        'product.product',
        domain="[('detailed_type', '=', 'service')]",
        related='company_id.second_whole_discount_product_id',
        readonly=0
    )
