from odoo import models, fields, api, _
import datetime


from odoo.exceptions import ValidationError

# from odoo.odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "cancel appointment wizard"

    appointment_id = fields.Many2one('hospital.appointment', string='appointment',
                                     domain="['|',('state', '=', 'draft'),('priority','in',('0',False))]")
    cancellation_date = fields.Date(string="cancellation_date", )
    reason = fields.Text(string='reason')

    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['cancellation_date'] = datetime.date.today()
        print(self.env.context)
        if self.env.context.get('active_id'):

            res['appointment_id'] = self.env.context.get('active_id')

        return res

    def action_cancel(self):
        print(self.env.context.get('active_id'))
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_(" sorry cancellation  not allowed on the same day of booking day"))
        self.appointment_id.state  = 'cancel'

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
