from odoo import api, fields, models, _


class HRContract(models.Model):
    _inherit = 'hr.contract'

    total_salary = fields.Float(
        compute="_compute_total_salary"
    )

    def _compute_total_salary(self):
        for rec in self:
            rec.total_salary = rec.l10n_sa_housing_allowance + rec.l10n_sa_transportation_allowance + rec.wage


