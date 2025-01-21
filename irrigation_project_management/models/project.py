""" Initialize Project """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
import math

import ast
import json
from pytz import UTC
from collections import defaultdict
from datetime import timedelta, datetime, time
from random import randint

from odoo import api, Command, fields, models, tools, SUPERUSER_ID, _, _lt
from odoo.addons.rating.models import rating_data
from odoo.addons.web_editor.controllers.main import handle_history_divergence
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.osv import expression
from odoo.tools.misc import get_lang


class ProjectProject(models.Model):
    """
        Inherit Project Project:
         -
    """
    _inherit = 'project.project'
    _rec_name = 'code'

    name = fields.Char(required=0, tracking=False)
    code = fields.Char(
        'Project Code',
        tracking=True
    )
    project_code = fields.Char()
    customer_code = fields.Char(
        related='partner_id.ref',
        string='Customer Code',
        store=1
    )
    project_type_id = fields.Many2one(
        'project.type'
    )
    project_service_ids = fields.Many2many(
        'project.service',
        string='Required Services'
    )
    project_team_lead_id = fields.Many2one(
        'res.users',
        'Project Team Lead'
    )
    received_date = fields.Date()
    estimate_time = fields.Float()
    spent_time = fields.Float(
        compute='_compute_spent_time'
    )
    apply_qc = fields.Boolean()
    project_source_file_ids = fields.Many2many(
        'ir.attachment',
        'project_source_file_attachment',
        'project_source_file',
        'attachment_id'
    )
    done_tasks = fields.Integer(
        compute='_compute_done_tasks'
    )
    maximum_daily_working_hours = fields.Integer()
    grass_layout_ids = fields.Many2many(
        'ir.attachment',
        'grass_layout_attachment',
        'grass_layout',
        'attachment_id'
    )
    palm_and_tree_layout_ids = fields.Many2many(
        'ir.attachment',
        'palm_and_tree_layout_attachment',
        'palm_and_tree_layout',
        'attachment_id'
    )
    project_package_layout_ids = fields.Many2many(
        'ir.attachment',
        'project_package_layout_attachment',
        'project_package_layout',
        'attachment_id',
        string='Project Final Package'
    )
    project_frame = fields.Many2many(
        'ir.attachment',
        'project_frame_attachment',
        'project_frame_l',
        'attachment_id',
    )
    g_and_s_layout_ids = fields.Many2many(
        'ir.attachment',
        'pgand_ts_layout_attachment',
        'g_and_se_layout',
        'attachment_id',
        string='G & S'
    )
    grass = fields.Integer()
    ground_covers_low= fields.Integer()
    ground_covers_medium= fields.Integer()
    ground_covers_high= fields.Integer()
    shrubs_heavy_1 = fields.Integer(
        'Shrubs (Heavy)'
    )
    shrubs_separated_1 = fields.Integer(
        'Shrubs (Separated)'
    )
    trees_low= fields.Integer()
    trees_medium= fields.Integer()
    trees_high= fields.Integer()
    palms = fields.Integer()
    palms_like = fields.Integer()
    mainline_pipe = fields.Integer()
    laterals_pipe = fields.Integer()
    valve = fields.Char()
    controller = fields.Char()
    central_control = fields.Char()
    sensor_1 = fields.Char(
        'Sensor (1)'
    )
    sensor_2 = fields.Char(
        'Sensor (2)'
    )
    stage_id = fields.Many2one(
        groups=''
    )
    pumps = fields.Char()
    filters = fields.Char()
    fertigation = fields.Char()
    master_controller = fields.Char()
    grass_area = fields.Integer()
    palm = fields.Integer()
    tree = fields.Integer()
    palm_like = fields.Integer()
    ground_cover = fields.Integer()
    shrubs_separated = fields.Integer()
    shrubs_heavy = fields.Integer()
    estimated_sprinkler_valves = fields.Integer()
    estimated_bubblers_valves = fields.Integer()
    estimated_drips_valves = fields.Integer()
    actual_sprinkler_valves = fields.Integer()
    actual_bubblers_valves = fields.Integer()
    actual_drips_valves = fields.Integer()
    can_edit_project = fields.Boolean(
        compute='_compute_can_edit_project'
    )
    boq_item_line_ids = fields.One2many(
        'boq.item.line',
        'project_id'
    )
    category_id = fields.Many2one(
        'product.category'
    )
    raincad_database = fields.Text(
        'RainCAD Database'
    )
    soft_scape_data_ids = fields.One2many(
        'soft.scape.data',
        'project_id'
    )
    soft_scape_read = fields.Boolean(
        compute='_compute_soft_scape_read'
    )
    man_days = fields.Integer(
        'Man Days rate/ Valves'
    )
    total_estimated_valve = fields.Integer(
        'Total Estimated Valve number',
        compute='_compute_total_estimated_valve'
    )
    total_actual_valve = fields.Integer(
        'Total Actual Valve',
    )
    total_estimated_design = fields.Float(
        'Total Estimated Design',
        compute='_compute_total_estimated_design'
    )
    project_daily_water = fields.Float(
        'Project Daily Water Requirement (M³ / Day)',
        compute='_compute_project_daily_water'
    )
    
    project_pump_flow = fields.Float(
        'Estimated Pump flow rate (M³/Hr.) ( Run time 8 Hr.)',
        compute='_compute_project_pump_flow'
    )

    def project_update_all_action(self):
        action = self.env['ir.actions.act_window']._for_xml_id('project.project_update_all_action')
        action['display_name'] = _("%(name)s's Updates", name=self.code)
        return action

    def action_view_tasks_analysis(self):
        """ return the action to see the tasks analysis report of the project """
        action = self.env['ir.actions.act_window']._for_xml_id('project.action_project_task_user_tree')
        action['display_name'] = _("%(name)s's Tasks Analysis", name=self.code)
        action_context = ast.literal_eval(action['context']) if action['context'] else {}
        action_context['search_default_project_id'] = self.id
        return dict(action, context=action_context)

    def action_project_task_burndown_chart_report(self):
        action = self.env['ir.actions.act_window']._for_xml_id('project.action_project_task_burndown_chart_report')
        action['display_name'] = _("%(name)s's Burndown Chart", name=self.code)
        return action

    def action_project_timesheets(self):
        action = self.env['ir.actions.act_window']._for_xml_id('hr_timesheet.act_hr_timesheet_line_by_project')
        action['display_name'] = _("%(name)s's Timesheets", name=self.code)
        return action

    def action_view_all_rating(self):
        """ return the action to see all the rating of the project and activate default filters"""
        action = self.env['ir.actions.act_window']._for_xml_id('project.rating_rating_action_view_project_rating')
        action['display_name'] = _("%(name)s's Rating", name=self.code)
        action_context = ast.literal_eval(action['context']) if action['context'] else {}
        action_context.update(self._context)
        action_context['search_default_rating_last_30_days'] = 1
        action_context.pop('group_by', None)
        action['domain'] = [('consumed', '=', True), ('parent_res_model', '=', 'project.project'), ('parent_res_id', '=', self.id)]
        if self.rating_count == 1:
            action.update({
                'view_mode': 'form',
                'views': [(view_id, view_type) for view_id, view_type in action['views'] if view_type == 'form'],
                'res_id': self.rating_ids[0].id, # [0] since rating_ids might be > then rating_count
            })
        return dict(action, context=action_context)


    def action_get_list_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%(name)s's Milestones", name=self.code),
            'domain': [('project_id', '=', self.id)],
            'res_model': 'project.milestone',
            'views': [(self.env.ref('project.project_milestone_view_tree').id, 'tree')],
            'view_mode': 'tree',
            'help': _("""
                <p class="o_view_nocontent_smiling_face">
                    No milestones found. Let's create one!
                </p><p>
                    Track major progress points that must be reached to achieve success.
                </p>
            """),
            'context': {
                'default_project_id': self.id,
                **self.env.context
            }
        }

    def action_view_tasks(self):
        action = self.env['ir.actions.act_window'].with_context({'active_id': self.id})._for_xml_id('project.act_project_project_2_project_task_all')
        action['display_name'] = _("%(name)s", name=self.code)
        context = action['context'].replace('active_id', str(self.id))
        context = ast.literal_eval(context)
        context.update({
            'create': self.active,
            'active_test': self.active
        })
        action['context'] = context
        return action

    @api.depends('soft_scape_data_ids')
    def _compute_total_estimated_valve(self):
        """ Compute total_estimated_valve value """
        for rec in self:
            if rec.soft_scape_data_ids:
                rec.total_estimated_valve = math.ceil(sum(rec.soft_scape_data_ids.mapped('evn')))
            else:
                rec.total_estimated_valve = 0

    @api.depends('soft_scape_data_ids')
    def _compute_project_daily_water(self):
        """ Compute total_estimated_valve value """
        for rec in self:
            if rec.soft_scape_data_ids:
                rec.project_daily_water = sum(rec.soft_scape_data_ids.mapped('wr'))
            else:
                rec.project_daily_water = 0

    @api.depends('man_days', 'total_estimated_valve')
    def _compute_total_estimated_design(self):
        """ Compute total_estimated_design value """
        for rec in self:
            if rec.man_days:
                rec.total_estimated_design = (rec.total_estimated_valve / rec.man_days) * 6
            else:
                rec.total_estimated_design = 0
    
    @api.depends('task_ids')
    def _compute_done_tasks(self):
        """ Compute done_tasks value """
        for rec in self:
            if rec.task_ids:
                rec.done_tasks = len(rec.task_ids.filtered(lambda x:x.stage_id.is_done))
            else:
                rec.done_tasks = 0

    @api.depends('project_daily_water')
    def _compute_project_pump_flow(self):
        """ Compute project_pump_flow value """
        for rec in self:
            rec.project_pump_flow = rec.project_daily_water / 8
    
    def add_products(self):
        """ Add Products """
        for rec in self:
            products = self.env['product.product'].search([
                ('categ_id', '=', rec.category_id.id)
            ])
            if products:
                for pro in products:
                    self.env['boq.item.line'].create({
                        'product_id': pro.id,
                        'category_id': rec.category_id.id,
                        'project_id': rec.id,
                        'internal_code': pro.default_code,
                    })

    def action_task_attachment(self):

        attachment = self.env['task.attachment'].search([('task_id.project_id', '=', self.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': _('Task Attachments'),
            'res_model': 'task.attachment',
            'view_type': 'list',
            'view_mode': 'list',
            'view_ids': [(False, 'list')],
            'view_id': self.env.ref('irrigation_project_management.task_attachment_tree').id,
            'domain': [('id', 'in', attachment.ids)],
        }

    def send_to_boq_items(self):
        """ Send To Boq Items """
        for rec in self:
            if rec.soft_scape_data_ids:
                for line in rec.soft_scape_data_ids:
                    products = self.env['product.product'].search([
                        ('categ_id', 'in', line.category_ids.ids),
                        ('brand_id', '=', line.brand_id.id),
                    ])
                    if products:
                        for pro in products:
                            self.env['boq.item.line'].create({
                                'planet_type_id': line.planet_type_id.id,
                                'product_id': pro.id,
                                'category_id': pro.categ_id.id,
                                'project_id': rec.id,
                                'internal_code': pro.default_code,
                                'qty_est': line.es_qty,
                            })

    @api.model
    def create(self, vals_list):
        """
            Override create method
             - sequence name
        """
        sequence = self.env['ir.sequence'].next_by_code('project.code')
        vals_list.update(project_code=sequence or '/')
        return super(ProjectProject, self).create(vals_list)

    def _compute_can_edit_project(self):
        """ Compute can_edit_project value """
        for rec in self:
            if self.env.user.has_group('project.group_project_manager'):
                rec.can_edit_project = True
            else:
                rec.can_edit_project = False

    def _compute_soft_scape_read(self):
        """ Compute can_edit_project value """
        for rec in self:
            if self.env.user.has_group('project.group_project_manager') or self.env.user.has_group('irrigation_project_management.group_pm') or self.env.user.has_group('irrigation_project_management.group_qs'):
                rec.soft_scape_read = True
            else:
                rec.soft_scape_read = False

    @api.depends('task_ids')
    def _compute_spent_time(self):
        """ Compute spent_time value """
        for rec in self:
            if rec.task_ids:
                rec.spent_time = sum(rec.task_ids.mapped('effective_hours'))
            else:
                rec.spent_time = 0