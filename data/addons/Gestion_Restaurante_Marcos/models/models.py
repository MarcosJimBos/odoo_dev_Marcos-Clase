import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class Plato(models.Model):
    _name = "gestion_restaurante_marcos.plato"
    _description = "Plato"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre del plato")
    precio = fields.Float(string="Precio (€)", required=True, help="Precio del plato")
    tiempo_preparacion = fields.Integer(string="Tiempo de preparación (min)")
    disponible = fields.Boolean(string="Disponible", default=True)
    categoria = fields.Selection([
        ('entrante', 'Entrante'),
        ('principal', 'Plato principal'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida')
    ], string="Categoría", required=True)

    menu = fields.Many2one(
        "gestion_restaurante_marcos.menu",
        string="Menú",
        ondelete="set null"
    )

    rel_ingredientes = fields.Many2many(
        "gestion_restaurante_marcos.ingrediente",
        "plato_ingrediente_rel",
        "plato_id",
        "ingrediente_id",
        string="Ingredientes"
    )

    # LOGS
    def create(self, vals):
        _logger.info("🍽️ Creando plato: %s", vals.get("nombre"))
        return super().create(vals)

    def write(self, vals):
        _logger.info("✏️ Modificando plato: %s", self.nombre)
        return super().write(vals)

    def unlink(self):
        for rec in self:
            _logger.info("🗑️ Eliminando plato: %s", rec.nombre)
        return super().unlink()


class Menu(models.Model):
    _name = "gestion_restaurante_marcos.menu"
    _description = "Menú"

    nombre = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    fecha_inicio = fields.Date(string="Fecha inicio", required=True)
    fecha_fin = fields.Date(string="Fecha fin")
    activo = fields.Boolean(string="Activo", default=True)

    platos = fields.One2many(
        "gestion_restaurante_marcos.plato",
        "menu",
        string="Platos del menú"
    )

    # LOGS
    def create(self, vals):
        _logger.info("📋 Creando menú: %s", vals.get("nombre"))
        return super().create(vals)

    def unlink(self):
        for rec in self:
            _logger.info("🗑️ Eliminando menú: %s", rec.nombre)
        return super().unlink()


class Ingrediente(models.Model):
    _name = "gestion_restaurante_marcos.ingrediente"
    _description = "Ingrediente"

    nombre = fields.Char(string="Nombre", required=True)
    es_alergeno = fields.Boolean(string="Es alérgeno")
    descripcion = fields.Text(string="Descripción")

    platos = fields.Many2many(
        "gestion_restaurante_marcos.plato",
        "plato_ingrediente_rel",
        "ingrediente_id",
        "plato_id",
        string="Platos"
    )

    # LOG
    def create(self, vals):
        _logger.info("🧄 Creando ingrediente: %s", vals.get("nombre"))
        return super().create(vals)
