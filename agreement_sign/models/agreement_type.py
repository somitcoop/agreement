from odoo import fields, models

class AgreementType(models.Model):
    _inherit = 'agreement.type'

    sign_template_id = fields.Many2one(
        'sign.oca.template',
        string='Default Sign Template',
        help='Default template to use for signing agreements of this type',
    )
