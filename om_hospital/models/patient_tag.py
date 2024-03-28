from odoo import models, fields, api, _
from datetime import date


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient.tag"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True,copy =False)
    color = fields.Integer(string='color')
    color_2 = fields.Char(string='color_2')
    sequence = fields.Integer(string="Sequence", )

    _sql_constraints = [
        ('name_tag_uniq', 'unique (name,active)', 'name must be unique '),
        ('name_tag_sequence', 'check (sequence > 0)', 'sequence must be bigger than 0 ')

    ]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + '(copy)'
        default['sequence'] = 10
        return super(PatientTag, self).copy(default)
