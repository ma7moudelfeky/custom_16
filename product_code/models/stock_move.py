""" Initialize Model """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class StockMove(models.Model):
    """
        Inherit Stock Move:
         -
    """
    _inherit = 'stock.move'

    product_code = fields.Char()


class StockMoveLine(models.Model):
    """
        Inherit Stock Move Line:
         -
    """
    _inherit = 'stock.move.line'

    product_code = fields.Char()
