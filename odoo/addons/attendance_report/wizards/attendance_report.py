# -*- coding: utf-8 -*-

"""
# Wizard untuk generate rekap presensi
# author @CakJuice <hd.brandoz@gmail.com>
"""

from datetime import datetime
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

class AttendanceReportWizard(models.TransientModel):
	_name = 'cj.attendance.report.wizard'

	date_start = fields.Date(string="Tanggal Awal", required=True, default=fields.Date.today)
	date_end = fields.Date(string="Tanggal Akhir", required=True, default=fields.Date.today)

	@api.multi
	def get_report(self):
		report_obj = self.env['report']
		template = 'cj_tutor_report.attendance_custom_report_view'
		report = report_obj._get_report_from_name(template)
		
		domain = {
			'date_start': self.date_start,
			'date_end': self.date_end,
		}
		
		vals = {
			'ids': self.ids,
			'model': report.model,
			'form': domain
		}

		"""get_action() otomatis akan memanggil render_html() di report"""
		return report_obj.get_action(self, template, data=vals)

class ReportAttendanceCustom(models.AbstractModel):
	"""
	# Report untuk menggenerate custom report
	# _name diisi dengan pola 'report.module_name.report_name'
	# _template diisi dengan pola 'module_name.report_name'
	"""

	_name = 'report.cj_tutor_report.attendance_custom_report_view'
	_template = 'cj_tutor_report.attendance_custom_report_view'

	@api.model
	def render_html(self, docids, data=None):
		if data is None:
			return

		date_start = data['form']['date_start']
		date_end = data['form']['date_end']

		report_obj = self.env['report']
		docs = self._get_rekap_data(date_start, date_end)

		LOCAL_FORMAT = '%d/%m/%Y'

		vals = {
			'docs': docs,
			'date_start': datetime.strptime(date_start, DATE_FORMAT).strftime(LOCAL_FORMAT),
			'date_end': datetime.strptime(date_end, DATE_FORMAT).strftime(LOCAL_FORMAT),
		}

		return report_obj.render(self._template, values=vals)

	def _get_rekap_data(self, date_start, date_end):
		"""
		return [
			{
				'employee': "employee 1 name",
				'presensi': count_of_presence,
				'absensi': count_of_absence,
			},
			{
				'employee': "employee 2 name",
				'presensi': count_of_presence,
				'absensi': count_of_absence,
			}
		]
		""" 

		date_start_obj = datetime.strptime(date_start, DATE_FORMAT).date()
		date_end_obj = datetime.strptime(date_end, DATE_FORMAT).date()
		date_count = (date_end_obj - date_start_obj).days + 1
		
		data = []

		# get all employee_data
		employees = self.env['hr.employee'].search([], order='name asc')
		for employee in employees:
			attendance_count = self.env['hr.attendance'].search_count([
				('employee_id', '=', employee.id),
				('check_in', '>=', date_start),
				('check_in', '<=', date_end)
			])

			selisih = date_count - attendance_count

			data.append({
				'employee': employee.name,
				'presensi': str(attendance_count) if attendance_count > 0 else '-',
				'absensi': str(selisih) if selisih > 0 else '-'
			})

		return data