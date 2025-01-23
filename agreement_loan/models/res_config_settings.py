# account_loan_permanent/models/res_config_settings.py

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    default_loan_agreement_template_id = fields.Many2one(
        comodel_name="agreement",
        string="Default Loan Agreement Template",
        related="company_id.default_loan_agreement_template_id",
        domain=[("is_template", "=", True)],
        help="Default template for loan agreements",
        readonly=False,
        default_model="agreement",
    )

