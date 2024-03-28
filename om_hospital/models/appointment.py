from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital appointment"
    _rec_name = 'name_seq'
    _order = 'id desc'

    name_seq = fields.Char(string="name", readonly=True, )
    patient_id = fields.Many2one('hospital.patient', string="patient", ondelete='restrict')
    gender = fields.Selection(related='patient_id.gender', readonly=False)
    age = fields.Integer(string="Age", related='patient_id.age')
    appointment_time = fields.Datetime(string="appointment time", default=fields.Datetime.now)
    booking_date = fields.Date(string="booking date", default=fields.Date.context_today)
    ref = fields.Char(string="Reference", help="reference of patient from patient records")
    prescription = fields.Html(string='prescription')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High'), ('4', 'Excellent')],
                                string='Priority')
    state = fields.Selection(
        [('draft', 'draft'), ('in_consultation', 'In_consultation'), ('done', 'Done'), ('cancel', 'Cancelled')],
        string='state', default='draft', required=True)
    doctor_id = fields.Many2one('res.users', string="doctor")
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string='hide sales price')
    progress = fields.Integer(compute="_compute_progress")
    duration = fields.Float()

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref

    @api.model
    def create(self, vals):

        vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        print(vals)
        return super(HospitalAppointment, self).create(vals)

    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("you cannot delete appointment with Done states"))

        return super(HospitalAppointment, self).unlink()

    def action_test(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new  ',
            'url': 'https://www.facebook.com/?locale=ar_AR',
        }


    def action_in_consultation(self):
        # print(self)
        for r in self:
            if r.state == "draft":
                r.state = 'in_consultation'

    def action_draft(self):
        for r in self:
            r.state = 'draft'

    def action_done(self):
        for r in self:
            r.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'shehab nasser',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        for r in self:
            r.state = 'cancel'

    def test_action(self):
        pass

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "appointment pharmacy lines"

    product_id = fields.Many2one('product.product')
    price_unit = fields.Float(string='price', related='product_id.list_price')
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='appointment')
    # price_subtotal = fields.Monetary(string ="price subtotal" )
