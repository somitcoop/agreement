from odoo import fields, models

class SignOcaRequest(models.Model):
    _inherit = 'sign.oca.request'

    agreement_id = fields.Many2one(
        'agreement',
        string='Agreement',
        ondelete='cascade',
    )
