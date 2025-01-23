from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    default_subscription_agreement_template_id = fields.Many2one(
        comodel_name='agreement',
        string='Default Subscription Agreement Template',
        domain=[('is_template', '=', True)],
        help='Default template for subscription agreements',
    )
