from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)

class Agreement(models.Model):
    _inherit = 'agreement'

    pdf_document = fields.Binary(
        string='PDF Document',
        attachment=True,
        copy=False,
    )

    def _get_report_pdf(self):
        """Generate PDF report for agreement"""
        self.ensure_one()
        try:
            report_action = self.env['ir.actions.report'].search([
                ('report_name', '=', 'agreement_legal.report_agreement_document'),
                ('report_type', '=', 'qweb-pdf'),
                ('model', '=', 'agreement')
            ], limit=1)

            if not report_action:
                raise UserError(_("PDF report action not found"))

            pdf_content, _ = report_action._render_qweb_pdf(self.id)

            if not pdf_content:
                raise UserError(_("Failed to generate PDF content"))

            return pdf_content

        except UserError as e:
            _logger.error("Error generating PDF for agreement %s: %s", self.id, str(e))
            raise
        except Exception as e:
            _logger.error("Unexpected error generating PDF for agreement %s: %s", self.id, str(e))
            raise UserError(_("Error generating PDF: %s") % str(e))

    def _get_cached_pdf(self):
        if not self.pdf_document:
            pdf_content = self._get_report_pdf()
            self.pdf_document = base64.b64encode(pdf_content)
        return base64.b64decode(self.pdf_document)

    def action_create_sign_request(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_("Please set a partner before creating signature request"))

        # Generar PDF desde el acuerdo
        pdf_content = self._get_report_pdf()

        # Crear plantilla de firma para este acuerdo específico
        template_vals = {
            'name': f'Sign Template - {self.name}',
            'model_id': self.env.ref('agreement_legal.model_agreement').id,
            'data': pdf_content,
        }
        sign_template = self.env['sign.oca.template'].create(template_vals)

        # Añadir campo de firma en la última página
        self.env['sign.oca.template.item'].create({
            'template_id': sign_template.id,
            'role_id': self.env.ref('agreement_sign.sign_role_agreement').id,
            'field_id': self.env.ref('sign_oca.sign_field_signature').id,
            'page': -1,  # Última página
            'position_x': 10,
            'position_y': 90,
            'width': 40,
            'height': 10,
            'required': True,
        })

        # Crear solicitud de firma
        sign_request = self.env['sign.oca.request'].create({
            'template_id': sign_template.id,
            'name': self.name,
            'data': pdf_content,
            'record_ref': f'{self._name},{self.id}',
            'signer_ids': [(0, 0, {
                'role_id': self.env.ref('agreement_sign.sign_role_agreement').id,
                'partner_id': self.partner_id.id,
            })],
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sign.oca.request',
            'res_id': sign_request.id,
            'view_mode': 'form',
            'target': 'current',
        }
