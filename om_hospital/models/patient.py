from dateutil import relativedelta

from odoo import models, fields, api, _
from datetime import date

from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string="Name", tracking=True)
    ref = fields.Char(string="Reference", tracking=True)
    age = fields.Integer(string="Age", tracking=True, compute='_compute_age',
                         inverse='_inverse_compute_age', search='_search_age', )
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    birth_day = fields.Date(string='Birthday')
    image = fields.Image(string='image')
    tag_ids = fields.Many2many('patient.tag', string='tags')
    appointment_count = fields.Char(string="Appointment count ", compute="_compute_appointment_count", store=True,
                                    )
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id')
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([
        ('married', 'married'),
        ('single', 'single'), ], string='marital status')
    partner_name = fields.Char(string="partner Name")
    is_birthday = fields.Boolean(compute="_is_birthday_compute")
    phone = fields.Char()
    email = fields.Char()
    website = fields.Char()

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        # print(self.)
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("you cannt delete patient with appointment"))

    def _compute_appointment_count(self):
        for rec in self:
            appointment_group = self.env['hospital.appointment'].read_group(domain=[], fields=['patient_id'],
                                                                            groupby=['patient_id'])
            for appointment in appointment_group:
                patient_id = appointment.get('patient_id')[0]
                patient_rec = self.browse(patient_id)
                patient_rec.appointment_count = appointment['patient_id_count']
                self -= patient_rec
            self.appointment_count = 0

    @api.constrains('birth_day')
    def check_birth_day(self):
        for rec in self:
            if rec.birth_day and rec.birth_day > fields.Date.today():
                raise ValidationError(_("entered of birth_day is not acceptable "))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        print(vals)
        return super(HospitalPatient, self).create(vals)

    # @api.model
    # def write(self, vals):
    #     if not vals['ref']:
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
    #     return super(HospitalPatient, self).write(vals)

    def name_get(self):
        return [(record.id, "[%s]:%s" % (record.ref, record.name)) for record in self]

    @api.depends('birth_day')
    def _compute_age(self):
        for r in self:
            today = date.today()
            if r.birth_day:
                r.age = today.year - r.birth_day.year
            else:
                r.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.birth_day = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        birth_day = date.today() - relativedelta.relativedelta(years=value)
        return [('birth_day', '=', birth_day)]

    @api.depends('birth_day')
    def _is_birthday_compute(self):
        is_birthday = False
        for rec in self:
            if rec.birth_day:
                today = date.today()
                if today.day == rec.birth_day.day and today.month == rec.birth_day.month:
                    is_birthday = True
            rec.is_birthday = is_birthday
    def action_view_appointment (self):
        return {
            'name': _('Appointment'),
            'view_mode': 'list,form',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'res_id': self.id,
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {}
        }
