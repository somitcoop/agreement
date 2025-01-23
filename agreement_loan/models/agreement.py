# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Agreement(models.Model):
    _inherit = 'agreement'

    loan_id = fields.Many2one(
        'account.loan',
        string='Loan',
        help='Loan associated with this agreement',
    )
