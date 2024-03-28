from odoo import api, fields, models
from odoo.odoo.tools.convert import safe_eval


class odooPlayground(models.Model):
    _name = "odoo.playground"
    _description = "odoo playground"
    DEFAULT_STRING = """
    # you want to capture a specific window,
    # click on the window to make it active and then press the "Alt" key + 
    # "Print Screen" keys. Open any image editor (e.g., Paint, Photoshop) and 
    # press "Ctrl" + "V" to paste the captured screenshot.

    """

    model_id = fields.Many2one('ir.model', string='model')
    code = fields.Text(string='code', default=DEFAULT_STRING)
    result = fields.Text(string="result", )

    def action_excute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)
