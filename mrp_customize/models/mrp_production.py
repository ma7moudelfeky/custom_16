""" Initialize Mrp Bom """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class TankTank(models.Model):
    """
        Initialize Tank Tank:
         -
    """
    _name = 'tank.tank'
    _description = 'Tank Tank'
    _check_company_auto = True

    name = fields.Char(
        required=True,
    )
    weight = fields.Float()


class MrpProduction(models.Model):
    """
        Inherit Mrp Bom:
         - 
    """
    _inherit = 'mrp.production'

    tank_id = fields.Many2one(
        'tank.tank'
    )
    tank_weight = fields.Float(
        related='tank_id.weight',
        # store=1,
        # readonly=0
    )
    unit_volume = fields.Float(
        # related='bom_id.unit_volume',
        # store=1,
        # readonly=0
    )
    no_of_products_on_unit = fields.Float()
    product_id = fields.Many2one(
        domain="[('bom_ids', '!=', False)]"
    )

    @api.onchange('tank_weight', 'unit_volume', 'no_of_products_on_unit')
    def _onchange_unit_volume(self):
        """  """
        for rec in self:
            if rec.tank_weight and rec.unit_volume:
                rec.product_qty = rec.tank_weight / rec.unit_volume
                for line in rec.move_raw_ids:
                    line._onchange_percent()

    def set_consumed_qty(self):
        """ Set Consumed Qty """
        for rec in self:
            # rec.qty_producing = rec.product_qty
            for line in rec.move_raw_ids:
                line.quantity_done = line.product_uom_qty


class StockMove(models.Model):
    """
        Inherit Mrp Bom Line:
         - 
    """
    _inherit = 'stock.move'
    
    percent = fields.Float(
        related='bom_line_id.percent',
        store=1,
        readonly=0
    )

    @api.onchange('percent','product_id', 'raw_material_production_id.tank_weight', 'raw_material_production_id.product_qty', 'rec.raw_material_production_id.no_of_products_on_unit')
    def _onchange_percent(self):
        """ percent """
        for rec in self:
            if rec.percent:
                rec.product_uom_qty = (rec.percent / 100) * rec.raw_material_production_id.tank_weight
            elif rec.product_id.is_carton and rec.raw_material_production_id.no_of_products_on_unit:
                rec.product_uom_qty = rec.raw_material_production_id.product_qty / rec.raw_material_production_id.no_of_products_on_unit
            else:
                rec.product_uom_qty = rec.raw_material_production_id.product_qty
