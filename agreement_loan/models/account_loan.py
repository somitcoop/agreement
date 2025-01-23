# account_loan_permanent/models/account_loan.py

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class AccountLoan(models.Model):
    _inherit = 'account.loan'

    agreement_id = fields.Many2one(
        'agreement',
        string='Agreement',
        copy=False,
    )
    end_date = fields.Date(
        string='End Date',
        compute='_compute_end_date',
        store=True,
    )

    @api.depends('start_date', 'periods', 'method_period')
    def _compute_end_date(self):
        for loan in self:
            if loan.start_date and loan.periods and loan.method_period:
                loan.end_date = loan.start_date + relativedelta(
                    months=loan.periods * loan.method_period
                )
            else:
                loan.end_date = False

    def _prepare_agreement_vals(self, template):
        """Prepare values for agreement creation"""
        self.ensure_one()
        agreement_type = self.env.ref('agreement_loan.agreement_type_loan')
        return {
            'name': f'Loan Agreement - {self.name}',
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'agreement_type_id': agreement_type.id or template.agreement_type_id.id,
            'description': template.description,
            'start_date': fields.Date.today(),
            'end_date': self.end_date,
            'company_partner_id': self.company_id.partner_id.id,
            'template_id': template.id,
            'loan_id': self.id,
        }

    def create_agreement(self):
        """Create agreement from template"""
        self.ensure_one()
        template_id = self.company_id.default_loan_agreement_template_id.id
        if not template_id:
            raise UserError(_('Please configure a default loan agreement template'))

        template = self.env['agreement'].browse(int(template_id))
        agreement_vals = self._prepare_agreement_vals(template)
        agreement = self.env['agreement'].create(agreement_vals)
        self.agreement_id = agreement.id

        # Enviar por email
        template_email = self.env.ref(
            'agreement_loan.email_template_loan_agreement'
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
