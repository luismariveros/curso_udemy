# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Update_wizard(models.TransientModel):
    _name = 'update_wizard'
    _description = _('Update_wizard')

    name = fields.Char(_('Nueva descripción'))

    def update_vista_general(self):
        _logger.info('################# Hello Wizard')
        presupuesto_obj = self.env['presupuesto']
        # presupuesto_id = presupuesto_obj.search([('id', '=', self._context['active_id'])])
        presupuesto_id = presupuesto_obj.browse(self._context['active_id'])
        presupuesto_id.vista_general = self.name
