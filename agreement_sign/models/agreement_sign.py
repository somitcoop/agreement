# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class AgreementSign(models.Model):
    _name = 'agreement.sign'
    _description = 'Agreement Sign'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(related='agreement_id.name', store=True)
    agreement_id = fields.Many2one(
        'agreement',
        string='Agreement',
        required=True,
        ondelete='cascade'
    )
    sign_template_id = fields.Many2one(
        'sign.oca.template',
        string='Sign Template',
        required=True
    )
    sign_request_id = fields.Many2one(
        'sign.oca.request',
        string='Sign Request',
        copy=False
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('signed', 'Signed'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    def action_send_for_signature(self):
        self.ensure_one()
        if not self.agreement_id.partner_id:
            raise ValidationError(_('Please set a partner in the agreement before sending for signature.'))

        # Create sign request
        vals = {
            'name': self.agreement_id.name,
            'template_id': self.sign_template_id.id,
            'data': self.agreement_id.signed_contract,
            'record_ref': f'agreement,{self.agreement_id.id}',
            'signer_ids': [(0, 0, {
                'role_id': self.env.ref('sign_oca.sign_role_customer').id,
                'partner_id': self.agreement_id.partner_id.id,
            })],
        }
        sign_request = self.env['sign.oca.request'].create(vals)
        self.write({
            'sign_request_id': sign_request.id,
            'state': 'sent'
        })
        sign_request.action_send()
        return True

    @api.model
    def _check_sign_request_status(self):
        """Cron job to check signature status"""
        signs = self.search([('state', '=', 'sent')])
        for sign in signs:
            if sign.sign_request_id.state == 'signed':
                sign.write({'state': 'signed'})
                sign.agreement_id.write({
                    'signed_contract': sign.sign_request_id.data,
                    'company_signed_date': fields.Date.today(),
                    'partner_signed_date': fields.Date.today(),
                })
