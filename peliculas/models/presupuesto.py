# -*- coding:utf-8 -*-
import logging
from odoo import fields, models, api, _
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class Presupuesto(models.Model):
    _name = "presupuesto"
    _description = _('Presupuesto')
    _inherit = ["image.mixin", "mail.thread", 'mail.activity.mixin']

    @api.depends('detalle_ids')
    def _compute_total(self):
        for record in self:
            subtotal = 0
            for linea in record.detalle_ids:
                subtotal += linea.importe
            record.base = subtotal
            record.impuestos = subtotal * 0.10
            record.total = subtotal * 1.10

    name = fields.Char(string="Pelicula")
    detalle_ids = fields.One2many(
        comodel_name="presupuesto.detalle",
        inverse_name="presupuesto_id",
        string="Detalles",
    )
    clasificacion = fields.Selection(
        selection=[
            ("G", "G"),  # publico en general
            ("PG", "PG"),  # se requiere compania de adulto
            ("PG-13", "PG-13"),
            ("R", "R"),
            ("NC-17", "NC-17"),
        ]
    )
    clasificacion_descripcion = fields.Char(string="Descripción")
    fecha_estreno = fields.Date(string="Estreno")
    puntuacion = fields.Integer(string="Puntuación", related="puntuacion2")
    puntuacion2 = fields.Integer()
    active = fields.Boolean(string="Activo", default=True)
    director_id = fields.Many2one(comodel_name="res.partner")
    categoria_director_id = fields.Many2one(
        comodel_name="res.partner.category",
        # segunda version
        default=lambda self: self.env.ref("peliculas.category_director"),
        # primera version
        # default=lambda self: self.env["res.partner.category"].search([("name", "=", "Director")])
    )
    actor_ids = fields.Many2many(comodel_name="res.partner", string="Actores")
    categoria_actor_id = fields.Many2one(
        comodel_name="res.partner.category",
        default=lambda self: self.env.ref("peliculas.category_actor"),
    )
    genero_ids = fields.Many2many(comodel_name="genero")
    vista_general = fields.Text(string="Descripción General")
    link_trailer = fields.Char(string="Trailer")
    es_libro = fields.Boolean(string="Version Libro")
    libro = fields.Binary(string="Libro")
    libro_filename = fields.Char(string="Nombre del libro")
    state = fields.Selection(
        selection=[
            ("borrador", "Borrador"),
            ("aprobado", "Aprobado"),
            ("cancelado", "Cancelado"),
        ],
        default="borrador",
        string="Estados",
        copy=False,
    )
    fecha_creacion = fields.Datetime(
        string="Fecha creacion",
        copy=False,
        default=lambda self: fields.Datetime.now(),
    )
    fecha_aprobado = fields.Datetime(string="Fecha aprobación", copy=False)
    presupuesto_numero = fields.Char(string="Presupuesto Nro.", copy=False)
    opinion = fields.Html(string="Opinion")
    campos_ocultos = fields.Boolean(string="Campos Ocultos")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id.id,
    )
    terminos = fields.Text(string="Términos")
    base = fields.Monetary(string="Base imponible", compute="_compute_total")
    impuestos = fields.Monetary(string="Impuestos", compute="_compute_total")
    total = fields.Monetary(string="Total", compute="_compute_total")

    def aprobar_presupuesto(self):
        logger.warning("hola aprobar")
        self.state = "aprobado"
        self.fecha_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        logger.warning("hola cancelar")
        self.state = "cancelado"

    def unlink(self):
        logger.info("******* entre en UNLINK")
        for record in self:
            if record.state != "cancelado":
                raise UserError(
                    "No se puede eliminar porque no está en CANCELADO"
                )
            super(Presupuesto, record).unlink()

    @api.model
    def create(self, vals_list):
        logger.info("**** Funcion CREATE variables:{0}".format(vals_list))
        sequence_obj = self.env["ir.sequence"]
        vals_list["presupuesto_numero"] = sequence_obj.next_by_code(
            "secuencia.presupuesto.pelicula"
        )
        return super(Presupuesto, self).create(vals_list)

    def write(self, vals_list):
        logger.info("**** Funcion WRITE variables:{0}".format(vals_list))
        if "clasificacion" in vals_list:
            raise UserError("La clasificacion no se puede editar")
        return super(Presupuesto, self).write(vals_list)

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = self.name + " (Copia)"
        default["puntuacion2"] = 1
        return super(Presupuesto, self).copy(default)

    @api.onchange("clasificacion")
    def _onchange_clasificacion(self):
        logger.info(
            "******* entre en ONCHANGE CLASIFICACION {0}".format(
                self.clasificacion
            )
        )
        if self.clasificacion:
            if self.clasificacion == "G":
                self.clasificacion_descripcion = "Publico General"
            if self.clasificacion == "PG":
                self.clasificacion_descripcion = (
                    "Se recomienda la compania de un adulto"
                )
            if self.clasificacion == "PG-13":
                self.clasificacion_descripcion = "Mayores de 13"
            if self.clasificacion == "R":
                self.clasificacion_descripcion = (
                    "En compania de un adulto obligatorio"
                )
            if self.clasificacion == "NC-17":
                self.clasificacion_descripcion = "Mayores de 18"
        else:
            self.clasificacion_descripcion = False


class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"
    _description = _('Detall Presupuesto')

    presupuesto_id = fields.Many2one(
        comodel_name="presupuesto", string="Presupuesto"
    )

    name = fields.Many2one(
        comodel_name="recurso.cinematografico", string="Recurso"
    )
    descripcion = fields.Char(string="Descripción", related="name.descripcion")
    contacto_id = fields.Many2one(
        comodel_name="res.partner", related="name.contacto_id"
    )
    imagen = fields.Binary(related="name.imagen")
    cantidad = fields.Float(default=1.0, digits=(16, 4))
    precio = fields.Float(digits="Product Price")
    importe = fields.Monetary()

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        related="presupuesto_id.currency_id",
    )

    @api.onchange("name")
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio
            self.importe = self.cantidad * self.precio

    @api.onchange("cantidad", "precio")
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio
