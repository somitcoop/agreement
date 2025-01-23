from odoo import fields, models
from odoo.tools.translate import _


class ResCompany(models.Model):
    _inherit = "res.company"

    default_loan_agreement_template_id = fields.Many2one(
        comodel_name='agreement',
        string='Default Loan Agreement Template',
        domain=[('is_template', '=', True)],
        help='Default template for loan agreements',
    )
