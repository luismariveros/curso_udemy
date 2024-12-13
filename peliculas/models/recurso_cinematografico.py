# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Recurso_cinematografico(models.Model):
    _name = "recurso.cinematografico"
    _description = "Recurso_Cinematografico"

    name = fields.Char("Recurso")
    descripcion = fields.Char(string="Descripción")
    precio = fields.Float(string="Precio")
    contacto_id = fields.Many2one(
        comodel_name="res.partner", domain="[('is_company','=',False)]"
    )
    imagen = fields.Binary(string="Imagen")
