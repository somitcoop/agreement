from odoo import models, fields

class Agreement(models.Model):
    _inherit = 'agreement'

    subscription_request_id = fields.Many2one(
        'subscription.request',
        string='Subscription Request',
        help='Subscription request associated with this agreement',
    )
