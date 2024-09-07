""" Initialize Account Move Inh """
# from arabic_reshaper import reshape
# from bidi.algorithm import get_display
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
class AccountMove(models.Model):
    """
        Inherit Account Move:
         - 
    """
    _inherit = 'account.move'

    invoice_user_id = fields.Many2one(
        string='Salesperson',
        comodel_name='res.users',
        copy=False,
        tracking=True,
        default=lambda self: self.env.user,
    )
    team_id = fields.Many2one(
        'crm.team', string='Sales Team',
        precompute=True,  # avoid queries post-create
        ondelete='set null', readonly=False, store=True)
    account_id = fields.Many2one('account.account', string='Account', ondelete='cascade',
                                 domain="[('deprecated', '=', False), ('company_id', '=', company_id), ('is_off_balance', '=', False)]",
                                 required=True, check_company=True)





