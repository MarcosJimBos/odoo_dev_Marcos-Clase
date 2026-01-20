import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# =====================================
# LOGGER
# =====================================
_logger = logging.getLogger(__name__)


# =====================================
# MODELO: PLATO
# =====================================
class Plato(models.Model):
    _name = "gestion_restaurante_marcos.plato"
    _description = "Plato"

    nombre = fields.Char(string="Nombre", required=True)
    precio = fields.Float(string="Precio (€)", required=True)
    tiempo_preparacion = fields.Integer(string="Tiempo de preparación (min)")
    disponible = fields.Boolean(string="Disponible", default=True)

    # 🔑 NECESARIO para el One2many del menú
    menu = fields.Many2one(
        "gestion_restaurante_marcos.menu",
        string="Menú"
    )

    categoria = fields.Many2one(
        "gestion_restaurante_marcos.categoria",
        string="Categoría",
        required=True
    )

    chef = fields.Many2one(
        "gestion_restaurante_marcos.chef",
        string="Chef"
    )

    chef_especializado = fields.Many2one(
        "gestion_restaurante_marcos.chef",
        compute="_compute_chef_especializado",
        store=True,
        string="Chef especializado"
    )

    especialidad_chef = fields.Char(
        compute="_compute_especialidad_chef",
        store=True,
        string="Especialidad del chef"
    )

    ingredientes_ids = fields.Many2many(
        "gestion_restaurante_marcos.ingrediente",
        "plato_ingrediente_rel",
        "plato_id",
        "ingrediente_id",
        string="Ingredientes"
    )

    @api.depends("categoria")
    def _compute_chef_especializado(self):
        for plato in self:
            if plato.categoria:
                chef = self.env["gestion_restaurante_marcos.chef"].search(
                    [("especialidad", "=", plato.categoria.id)],
                    limit=1
                )
                plato.chef_especializado = chef
            else:
                plato.chef_especializado = False

    @api.depends("chef")
    def _compute_especialidad_chef(self):
        for plato in self:
            plato.especialidad_chef = (
                plato.chef.especialidad.nombre
                if plato.chef and plato.chef.especialidad
                else False
            )

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


# =====================================
# MODELO: MENÚ
# =====================================
class Menu(models.Model):
    _name = "gestion_restaurante_marcos.menu"
    _description = "Menú"

    nombre = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    fecha_inicio = fields.Date(string="Fecha inicio", required=True)
    fecha_fin = fields.Date(string="Fecha fin", required=True)
    activo = fields.Boolean(string="Activo", default=True)

    platos = fields.One2many(
        "gestion_restaurante_marcos.plato",
        "menu",
        string="Platos del menú"
    )

    @api.constrains("fecha_inicio", "fecha_fin")
    def _check_fechas_menu(self):
        for menu in self:
            if menu.fecha_inicio and menu.fecha_fin:
                if menu.fecha_inicio > menu.fecha_fin:
                    raise ValidationError(
                        "La fecha de inicio no puede ser posterior a la fecha de fin."
                    )

    def create(self, vals):
        _logger.info("📋 Creando menú: %s", vals.get("nombre"))
        return super().create(vals)

    def write(self, vals):
        _logger.info("✏️ Modificando menú: %s", self.nombre)
        return super().write(vals)

    def unlink(self):
        for rec in self:
            _logger.info("🗑️ Eliminando menú: %s", rec.nombre)
        return super().unlink()


# =====================================
# MODELO: INGREDIENTE
# =====================================
class Ingrediente(models.Model):
    _name = "gestion_restaurante_marcos.ingrediente"
    _description = "Ingrediente"

    nombre = fields.Char(string="Nombre", required=True)
    es_alergeno = fields.Boolean(string="Es alérgeno")
    descripcion = fields.Text(string="Descripción")

    platos_ids = fields.Many2many(
        "gestion_restaurante_marcos.plato",
        "plato_ingrediente_rel",
        "ingrediente_id",
        "plato_id",
        string="Platos"
    )


# =====================================
# MODELO: CATEGORÍA
# =====================================
class Categoria(models.Model):
    _name = "gestion_restaurante_marcos.categoria"
    _description = "Categoría de platos"

    nombre = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")

    platos = fields.One2many(
        "gestion_restaurante_marcos.plato",
        "categoria",
        string="Platos"
    )

    ingredientes_comunes = fields.Many2many(
        "gestion_restaurante_marcos.ingrediente",
        compute="_compute_ingredientes_comunes",
        string="Ingredientes comunes"
    )

    @api.depends("platos", "platos.ingredientes_ids")
    def _compute_ingredientes_comunes(self):
        for categoria in self:
            ingredientes = self.env["gestion_restaurante_marcos.ingrediente"]
            for plato in categoria.platos:
                ingredientes |= plato.ingredientes_ids
            categoria.ingredientes_comunes = ingredientes




# =====================================
# MODELO: CHEF
# =====================================
class Chef(models.Model):
    _name = "gestion_restaurante_marcos.chef"
    _description = "Chef"

    nombre = fields.Char(string="Nombre", required=True)

    especialidad = fields.Many2one(
        "gestion_restaurante_marcos.categoria",
        string="Especialidad"
    )

    platos_asignados = fields.One2many(
        "gestion_restaurante_marcos.plato",
        "chef",
        string="Platos asignados"
    )
