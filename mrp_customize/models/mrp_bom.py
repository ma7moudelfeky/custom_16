""" Initialize Mrp Bom """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning

#
# class MrpBom(models.Model):
#     """
#         Inherit Mrp Bom:
#          -
#     """
#     _inherit = 'mrp.bom'
#
#     tank_weight = fields.Float()
#     unit_volume = fields.Float()
#     no_of_products_on_unit = fields.Float()
#
#     @api.onchange('tank_weight', 'unit_volume')
#     def _onchange_tank_weight(self):
#         """  """
#         for rec in self:
#             if rec.tank_weight and rec.unit_volume:
#                 rec.product_qty = rec.tank_weight / rec.unit_volume
#

class MrpBomLine(models.Model):
    """
        Inherit Mrp Bom Line:
         - 
    """
    _inherit = 'mrp.bom.line'
    
    percent = fields.Float()

    # @api.onchange('percent', 'bom_id.tank_weight', 'bom_id.unit_volume')
    # def _onchange_percent(self):
    #     """ percent """
    #     for rec in self:
    #         if rec.percent:
    #             rec.product_qty = (rec.percent / 100) * rec.bom_id.tank_weight
