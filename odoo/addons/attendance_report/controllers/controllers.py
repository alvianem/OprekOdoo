# -*- coding: utf-8 -*-
from odoo import http

# class CjTutorReport(http.Controller):
#     @http.route('/cj_tutor_report/cj_tutor_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cj_tutor_report/cj_tutor_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cj_tutor_report.listing', {
#             'root': '/cj_tutor_report/cj_tutor_report',
#             'objects': http.request.env['cj_tutor_report.cj_tutor_report'].search([]),
#         })

#     @http.route('/cj_tutor_report/cj_tutor_report/objects/<model("cj_tutor_report.cj_tutor_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cj_tutor_report.object', {
#             'object': obj
#         })