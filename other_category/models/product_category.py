""" Initialize Product Category """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ProductCategory(models.Model):
    """
        Inherit Product Category:
         - 
    """
    _inherit = 'product.category'
    
    for_others = fields.Boolean()