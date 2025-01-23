# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Agreement(models.Model):
    _inherit = 'agreement'

    campaign_id = fields.Many2one(
        'funding.campaign',
        string='Campaign',
        help='Campaign associated with this agreement',
    )
