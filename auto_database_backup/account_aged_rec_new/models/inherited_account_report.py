# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from odoo.tools.misc import format_date

from dateutil.relativedelta import relativedelta
from itertools import chain

class AccountAgedPartner(models.AbstractModel):
    _inherit = 'account.report'

    def export_to_pdf(self, options):
        if options.get('ar2'):
            self = self.with_context(ar2=1)
        return super().export_to_pdf(options)

    def export_to_xlsx(self, options, response=None):
        return super(AccountAgedPartner,self.with_context(ar2=options.get('ar2'))).export_to_xlsx(options, response)
    def _get_options(self, previous_options=None):
        options = super()._get_options(previous_options)
        print(previous_options)
        print(self.env.context)
        # if self.env.context.get('print_mode'):
        # is_ar2 = previous_options.get('ar2') or options.get('ar2')
        # if is_ar2 != 1:
        #     options['ar2'] = self.env.context.get('ar2')
        # if 'ar1' not in self.env.context and previous_options.get('ar2'):
        #     options['ar2'] = previous_options.get('ar2')
        # print(self.env.context)
        # print(options)
        if self.env.context.get('ar2') and not options.get('ar2'):
            options['ar2'] = self.env.context.get('ar2')

        return options
