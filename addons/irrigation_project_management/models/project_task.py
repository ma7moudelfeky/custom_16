""" Initialize Project Task """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ProjectTask(models.Model):
    """
        Inherit Project Task:
         -
    """
    _inherit = 'project.task'

    #
    # @api.model
    # def default_get(self, fields_list):
    #     res = super(ProjectTask, self).default_get(fields_list)
    #     res['user_ids'] = [(6, 0, self.env.user)]
    #     return res

    quantity = fields.Integer(
        compute='_compute_quantity',
        string='Actual Quantity'
    )
    estimated_time = fields.Float(
        compute='_compute_estimated_time',
    )
    date_deadline = fields.Datetime()
    task_quantity_ids = fields.One2many(
        'task.quantity',
        'project_task_id'
    )
    name_done = fields.Boolean(
        related='stage_id.not_readonly_task_type'
    )
    is_done = fields.Boolean(
        related='stage_id.is_done'
    )
    customer_code = fields.Char(
        related='partner_id.ref',
        string='Customer Code'
    )
    can_edit_project = fields.Boolean(
        compute='_compute_can_edit_project'
    )
    task_type_id = fields.Many2one(
        'task.type'
    )
    edit_assignee = fields.Boolean(
        # compute='_compute_edit_assignee'
    )
    task_attachment_ids = fields.One2many(
        'task.attachment',
        'task_id'
    )
    task_type_checklist_ids = fields.One2many(
        'task.type.checklist',
        'task_id'
    )

    @api.constrains('stage_id')
    def _onchange_stage_id_done(self):
        """ stage_id """
        for rec in self:
            if rec.stage_id and rec.is_done and rec.quantity <= 0:
                raise ValidationError('Please add your task quantity !')

    @api.onchange('task_type_id')
    @api.constrains('task_type_id')
    def _onchange_project_type_id(self):
        """ project_type_id """
        for rec in self:
            rec.name = rec.task_type_id.name
            rec.task_type_checklist_ids = [(5,)]
            list = []
            if rec.task_type_id and rec.task_type_id.task_type_checklist_ids:
                for line in rec.task_type_id.task_type_checklist_ids:
                    line = [0, 0, {
                        'task_id': rec.id,
                        'code': line.code,
                        'name': line.name,
                        'qc_comment': line.qc_comment,
                        'repetition': line.repetition,
                        'correction': line.correction,
                        'is_task': True,
                        'description_ar': line.description_ar,
                        'description_en': line.description_en,
                        'severity_level': line.severity_level,
                    }]
                    list.append(line)
                rec.task_type_checklist_ids = list


    # @api.depends('task_type_id', 'name')
    def _compute_can_edit_project(self):
        """ Compute can_edit_project value """
        if self.env.user.has_group('project.group_project_manager') or self.env.user.has_group('irrigation_project_management.group_pm'):
            self.can_edit_project = True
        else:
            self.can_edit_project = False

        if self.env.user.has_group('project.group_project_manager') or self.env.user.has_group('irrigation_project_management.group_team_leader') or self.env.user.has_group('irrigation_project_management.group_pm'):
            self.edit_assignee = True
        else:
            self.edit_assignee = False

    @api.depends('task_quantity_ids')
    def _compute_quantity(self):
        """ Compute quantity value """
        for rec in self:
            if rec.task_quantity_ids:
                rec.quantity = sum(rec.task_quantity_ids.mapped('qty'))
            else:
                rec.quantity = 0

    @api.depends('task_quantity_ids')
    def _compute_estimated_time(self):
        """ Compute estimated_time value """
        for rec in self:
            if rec.task_quantity_ids:
                rec.estimated_time = sum(rec.task_quantity_ids.mapped('total'))
            else:
                rec.estimated_time = 0


class TaskQuantity(models.Model):
    """
        Initialize Task Quantity:
         -
    """
    _name = 'task.quantity'
    _description = 'Task Quantity'

    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure',
        related='project_task_id.task_type_id.uom_id'
    )
    kpi = fields.Float(
        related='project_task_id.task_type_id.kpi'
    )
    qty = fields.Integer()
    project_task_id = fields.Many2one(
        'project.task',
        'Task'
    )
    project_id = fields.Many2one(
        related='project_task_id.project_id',
        store=1
    )
    create_uid = fields.Many2one(
        'res.users',
        string='Assignee'
    )
    date_deadline = fields.Datetime(
        related='project_task_id.date_deadline',
        store=1
    )
    project_state = fields.Many2one(
        related='project_id.stage_id',
        store=1
    )
    total = fields.Float(
        compute='_compute_total'
    )
    hour_required = fields.Float(
        compute='_compute_hour_required',
        store=1
    )
    hour_spent = fields.Float(
        compute='_compute_hour_spent',
        store=1
    )
    rate = fields.Float(
        compute='_compute_rate',
        store=1
    )
    
    @api.depends('qty', 'kpi', 'project_task_id', 'create_uid', 'date_deadline', 'project_state', 'create_date', 'write_uid', 'write_date')
    def _compute_total(self):
        """ Compute total value """
        for rec in self:
            if rec.kpi:
                rec.total = rec.qty / rec.kpi
            else:
                rec.total = 0

    @api.depends('total', 'qty', 'kpi', 'project_task_id', 'create_uid', 'date_deadline', 'project_state', 'create_date', 'write_uid', 'write_date')
    def _compute_hour_spent(self):
        """ Compute hour_spent value """
        for rec in self:
            if rec.project_task_id and rec.create_uid:
                time_sheet = self.env['account.analytic.line'].search([
                    ('task_id', '=', rec.project_task_id.id),
                    ('employee_id', '=', rec.create_uid.employee_id.id),
                ])
                if time_sheet:
                    rec.hour_spent = sum(time_sheet.mapped('unit_amount'))
                else:
                    rec.hour_spent = 0
            else:
                rec.hour_spent = 0

    @api.depends('total', 'qty', 'kpi', 'project_task_id', 'create_uid', 'date_deadline', 'project_state', 'create_date', 'write_uid', 'write_date')
    def _compute_hour_required(self):
        """ Compute hour_required value """
        for rec in self:
            if rec.kpi:
                rec.hour_required = rec.qty / rec.kpi
            else:
                rec.hour_required = 0

    @api.depends('hour_spent', 'hour_required', 'total')
    def _compute_rate(self):
        """ Compute rate value """
        for rec in self:
            if rec.hour_spent:
                rec.rate = round(rec.hour_required / rec.hour_spent, 2) * 100
            else:
                rec.rate = 0


class TaskAttachment(models.Model):
    """
        Initialize Task Attachment:
         - 
    """
    _name = 'task.attachment'
    _description = 'Task Attachment'

    task_id = fields.Many2one(
        'project.task'
    )
    attachment_ids = fields.Many2many(
        'ir.attachment'
    )
