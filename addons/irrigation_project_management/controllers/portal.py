# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from operator import itemgetter
from markupsafe import Markup

from odoo import conf, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR, AND
from odoo.addons.project.controllers.portal import ProjectCustomerPortal


class ProjectPortal(ProjectCustomerPortal):

    # def _task_get_searchbar_sortings(self, milestones_allowed):
    #     values = super()._task_get_searchbar_sortings(milestones_allowed)
    #     values['planned_date_begin'] = {'label': _('Planned Date'), 'order': 'planned_date_begin asc', 'sequence': 7}
    #     return values


    def _prepare_searchbar_sortings(self):
        """ Override _prepare_searchbar_sortings """
        res = super(ProjectPortal, self)._prepare_searchbar_sortings()
        res['stage'] = {'label': _('Stage'), 'order': 'stage_id desc'}
        res['date'] = {'label': _('Newest'), 'order': 'create_date desc'}
        return res

    def _project_get_searchbar_inputs(self):
        values = {
            'all': {'input': 'all', 'label': _('Search in All'), 'order': 1},
            'stage': {'input': 'stage', 'label': _('Search in Stages'), 'order': 2},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _project_get_searchbar_groupby(self):
        values = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'stage': {'input': 'stage_id', 'label': _('Stage'), 'order': 2},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))


    @http.route(['/my/projects', '/my/projects/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_projects(self, page=1, date_begin=None, date_end=None, sortby=None,groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        Project = request.env['project.project']
        domain = self._prepare_project_domain()

        searchbar_sortings = self._prepare_searchbar_sortings()
        searchbar_inputs = self._project_get_searchbar_inputs()
        searchbar_groupby = self._project_get_searchbar_groupby()

        if not sortby or sortby not in searchbar_sortings:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # projects count
        project_count = Project.search_count(domain)
        # pager
        if sortby == 'stage_id':
            sortby = 'date'
        pager = portal_pager(
            url="/my/projects",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=project_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        projects = Project.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_projects_history'] = projects.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'projects': projects,
            'page_name': 'project',
            'default_url': '/my/projects',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            # 'searchbar_groupby': searchbar_groupby,
            #
            # 'searchbar_inputs': searchbar_inputs,
            #
            # 'groupby': groupby,

        })
        return request.render("project.portal_my_projects", values)
