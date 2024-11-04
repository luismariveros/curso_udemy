# -*- coding:utf-8 -*-
from odoo import fields, models, api


class Presupuesto(models.Model):
    _name = "presupuesto"
    _inherit = ['image.mixin']

    name = fields.Char(string='Pelicula')
    clasificacion = fields.Selection(selection=[
        ('G', 'G'),  # publico en general
        ('PG', 'PG'),  # se requiere compania de adulto
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
    ])
    fecha_estreno = fields.Date(string='Estreno')
    puntuacion = fields.Integer()
    active = fields.Boolean(string='Activo', default=True)
    director_id = fields.Many2one(comodel_name='res.partner')
    genero_ids = fields.Many2many(comodel_name='genero')
    vista_general = fields.Text(string='Descripción')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Version Libro')
    libro = fields.Binary(string='Libro')
