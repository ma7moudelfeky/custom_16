""" Initialize Account Move Line """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
class AccountMoveLine(models.Model):
    """
        Inherit Account Move Line:
         - 
    """
    _inherit = 'account.move.line'
    duration = fields.Float(string='Duration')
