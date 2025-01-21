from odoo import _, api, fields, models, tools
import locale
import datetime
import logging

_logger = logging.getLogger(__name__)

TRANS_MONTH = {'January' : 'Enero',
               'February' : 'Febrero',
               'March' : 'Marzo',
               'April' : 'Abril',
               'May' : 'Mayo',
               'June' : 'junio',
               'July' : 'Julio',
               'August' : 'Agosto',
               'September' : 'Septiembre',
               'Octuber' : 'Octubre',
               'December' : 'Diciembre',
               'November' : 'Noviembre'}

class HrContract(models.Model):

    _inherit = 'hr.contract'

    

    def print_date(self):
        month = datetime.datetime.today().strftime('%B')
        _logger.info(month)
        return TRANS_MONTH.get(month,month)