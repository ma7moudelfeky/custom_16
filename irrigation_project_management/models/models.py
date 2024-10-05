""" Initialize Models """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
import math

class ProjectType(models.Model):
    """
        Initialize Project Type:
         - 
    """
    _name = 'project.type'
    _description = 'Project Type'
    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'Name must be unique'),
    ]
    
    name = fields.Char(
        required=True,
    )


class PlanetType(models.Model):
    """
        Initialize Planet Type:
         -
    """
    _name = 'planet.type'
    _description = 'Planet Type'
    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'Name must be unique'),
    ]

    name = fields.Char(
        required=True,
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure'
    )
    formula = fields.Float()
    category_ids = fields.Many2many(
        'product.category'
    )
    lpd = fields.Integer()
    lph = fields.Integer()
    vr = fields.Integer()

class ProjectTaskType(models.Model):
    """
        Inherit Project Task Type:
         -
    """
    _inherit = 'project.task.type'

    not_readonly_task_type = fields.Boolean()
    is_done = fields.Boolean()


class TaskType(models.Model):
    """
        Initialize Task Type:
         -
    """
    _name = 'task.type'
    _description = 'Task Type'
    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'Name must be unique'),
    ]

    name = fields.Char(
        required=True,
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure'
    )
    kpi = fields.Float()
    task_type_checklist_ids = fields.One2many(
        'task.type.checklist',
        'task_type_id'
    )


class TaskTypeChecklist(models.Model):
    """
        Initialize Task Type Checklist:
         -
    """
    _name = 'task.type.checklist'
    _description = 'Task Type Checklist'

    code = fields.Char()
    name = fields.Char()
    qc_comment = fields.Char()
    repetition = fields.Integer()
    correction = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        default='yes',
    )

    is_task = fields.Boolean()
    description_ar = fields.Char()
    description_en = fields.Char()
    severity_level = fields.Selection(
        [('minor', 'Minor'),
         ('major', 'Major'),
         ('critical', 'Critical')],
    )
    task_type_id = fields.Many2one(
        'task.type'
    )
    task_id = fields.Many2one(
        'project.task'
    )
    project_id = fields.Many2one(
        'project.project',
        related='task_id.project_id',
        store=1
    )

class ProjectService(models.Model):
    """
        Initialize Project Service:
         - 
    """
    _name = 'project.service'
    _description = 'Project Service'
    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'Name must be unique'),
    ]

    name = fields.Char(
        required=True,
    )


class SoftScapeData(models.Model):
    """
        Initialize Soft Scape Data:
         - 
    """
    _name = 'soft.scape.data'
    _description = 'Soft Scape Data'

    project_id = fields.Many2one(
        'project.project'
    )
    planet_type_id = fields.Many2one(
        'planet.type'
    )
    uom_id = fields.Many2one(
        related='planet_type_id.uom_id'
    )
    lpd = fields.Integer(
        # related='planet_type_id.lpd',
        store=1
    )
    lph = fields.Integer(
        # related='planet_type_id.lph',
        store=1
    )
    vr = fields.Integer(
        # related='planet_type_id.vr',
        store=1
    )
    category_ids = fields.Many2many(
        related='planet_type_id.category_ids'
    )
    qty = fields.Float(
        'SS-QTY'
    )
    device_no = fields.Integer(
        default=1
    )
    es_qty = fields.Float(
        'QTY-ES',
        compute='_compute_es_qty'
    )

    attachment_ids = fields.Many2many(
        'ir.attachment'
    )
    brand_id = fields.Many2one(
        'product.brand'
    )
    wr = fields.Float(
        'WR',
        compute='_compute_wr'
    )
    evf = fields.Float(
        'EVF',
        compute='_compute_evf'
    )
    evn = fields.Float(
        'EVN',
        compute='_compute_evn'
    )

    @api.onchange('planet_type_id')
    def _onchange_planet_type_id(self):
        """ planet_type_id """
        for rec in self:
            if rec.planet_type_id:
                rec.lpd = rec.planet_type_id.lpd
                rec.lph = rec.planet_type_id.lph
                rec.vr = rec.planet_type_id.vr

    @api.depends('qty', 'device_no')
    def _compute_es_qty(self):
        """ Compute es_qty value """
        for rec in self:
            rec.es_qty = rec.qty * rec.device_no

    @api.depends('es_qty', 'lpd')
    def _compute_wr(self):
        """ Compute  value """
        for rec in self:
            rec.wr = (rec.es_qty * rec.lpd) / 1000

    @api.depends('es_qty', 'lph')
    def _compute_evf(self):
        """ Compute  value """
        for rec in self:
            rec.evf = (rec.es_qty * rec.lph) / 1000

    @api.depends('evf', 'vr')
    def _compute_evn(self):
        """ Compute  value """
        for rec in self:
            if rec.vr:
                rec.evn = rec.evf / rec.vr
            else:
                rec.evn = 0


class BoqItemLine(models.Model):
    """
        Initialize Boq Item Line:
         -
    """
    _name = 'boq.item.line'
    _description = 'Boq Item Line'

    project_id = fields.Many2one(
        'project.project'
    )
    planet_type_id = fields.Many2one(
        'planet.type'
    )
    internal_code = fields.Char()
    category_id = fields.Many2one(
        'product.category',
        'Series'
    )
    product_id = fields.Many2one(
        'product.product',
        # domain="[('categ_id', '=', category_id)]"
    )
    qty_est = fields.Float(
        'QTY-ES'
    )
    qty_dwg = fields.Float(
        'QTY-DWG'
    )
    formula = fields.Float(
        related='product_id.formula'
    )
    qty_boq = fields.Float(
        'QTY-BOQ',
        compute='_compute_qty_boq'
    )
    awq = fields.Integer(
        'AWQ',
        compute='_compute_awq'
    )
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            if rec.product_id:
                rec.internal_code = rec.product_id.default_code

    @api.depends('formula', 'product_id', 'qty_dwg')
    def _compute_awq(self):
        """ Compute awq value """
        for rec in self:
            if rec.product_id and rec.product_id.length:
                rec.awq = math.ceil((rec.qty_dwg * (rec.formula / 100)) / rec.product_id.length)
            else:
                rec.awq = 0

    @api.depends('awq', 'product_id')
    def _compute_qty_boq(self):
        """ Compute qty_boq value """
        for rec in self:
            rec.qty_boq = rec.awq * rec.product_id.length
