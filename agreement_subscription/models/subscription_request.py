from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    agreement_id = fields.Many2one(
        'agreement',
        string='Agreement',
        copy=False,
        help='Agreement associated with this subscription request'
    )

    def _prepare_agreement_vals(self, template):
        """Prepare values for agreement creation"""
        self.ensure_one()
        agreement_type = self.env.ref('agreement_subscription.agreement_type_subscription')
        return {
            'name': f'Subscription Agreement - {self.name}',
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'agreement_type_id': agreement_type.id or template.agreement_type_id.id,
            'description': template.description,
            'start_date': self.date,
            'company_partner_id': self.company_id.partner_id.id,
            'template_id': template.id,
            'subscription_request_id': self.id,
        }

    def create_agreement(self):
        """Create agreement from template"""
        self.ensure_one()

        if self.agreement_id:
            raise UserError(_('This subscription already has an associated agreement.'))

        template_id = self.company_id.default_subscription_agreement_template_id.id
        if not template_id:
            raise UserError(_('Please configure a default subscription agreement template in company settings'))

        template = self.env['agreement'].browse(template_id)
        agreement_vals = self._prepare_agreement_vals(template)
        agreement = self.env['agreement'].create(agreement_vals)
        self.agreement_id = agreement.id

        # Send email notification
        template_email = self.env.ref(
            'agreement_subscription.email_template_subscription_agreement',
            raise_if_not_found=False
        )
        if template_email:
            template_email.send_mail(agreement.id)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'agreement',
            'res_id': agreement.id,
            'view_mode': 'form',
            'view_type': 'form',
        }
