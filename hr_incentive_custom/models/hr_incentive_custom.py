from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrIncentiveCustom(models.Model):
    _name = 'hr.incentive.custom'
    _description = "HR Incentive"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Sequence Number', readonly=True)
    incentive_type = fields.Many2one('hr.incentive.type', string='Incentive Type', required=True, store=True, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id", readonly=True)
    job_id = fields.Many2one('hr.job', string="Job", related="employee_id.job_id", readonly=True)
    date = fields.Date(string="Date", default=fields.Date.today(), help="Date", tracking=True)
    contract_id = fields.Many2one('hr.contract', string="Contract", related="employee_id.contract_id")
    incentive_amount = fields.Float(string='Incentive Amount', tracking=True)
    state = fields.Selection([('draft', 'Draft'),
                             ('submit', 'Submit'),
                             ('approve', 'Approved'),
                             ('cancel', 'Cancelled')], string="State", default='draft', tracking=True)
    note = fields.Text(string='Note', tracking=True)

    @api.constrains('employee_id')
    def check_contract(self):
        for record in self:
            if not record.contract_id:
                raise ValidationError(_(" This employee have no running contract."))
    
    @api.constrains('incentive_amount')
    def _check_incentive_amount(self):
        for record in self:
            if record.incentive_amount < 1:
                raise ValidationError(_(" Incentive amount must be greater than 0."))

    def submit(self):
        return self.sudo().write({
            'state': 'submit',
        })
    
    def approve(self):
        return self.sudo().write({
            'state': 'approve',
        })

    def cancel(self):
        return self.sudo().write({
            'state': 'cancel',
        })

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('hr.incentive.custom') or '/'
        values['name'] = seq
        return super(HrIncentiveCustom, self.sudo()).create(values)

    def unlink(self):
        for incentive in self.filtered(
                lambda incentive: incentive.state != 'draft'):
            raise UserError(
                _('You cannot delete Incentive request which is not in draft state.'))
        return super(HrIncentiveCustom, self).unlink()

class HrIncentiveType(models.Model):
    _name = 'hr.incentive.type'
    _description = "HR Incentive Type"

    name = fields.Char(string='Name', required=True, tracking=True)

class HrIncentiveEmployee(models.Model):
    _inherit = "hr.employee"

    def get_incentive(self, employee_id, payslip):
        incentive_id = self.env['hr.incentive.custom'].search([('employee_id', '=', employee_id.id),
                                                      ('state', '=', 'approve')])
        total_incentive_amount = 0.0

        for record in incentive_id:
            if payslip.date_from <= record.date <= payslip.date_to:
                total_incentive_amount = total_incentive_amount + record.incentive_amount
        
        return total_incentive_amount