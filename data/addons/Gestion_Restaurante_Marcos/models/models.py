from odoo import models, fields

class Plato(models.Model):
    _name = "gestion_restaurante_marcos.plato"
    _description = "Plato"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre del plato")
    precio = fields.Float(string="Precio (€)", required=True, help="Precio del plato")
    tiempo_preparacion = fields.Integer(string="Tiempo de preparación (min)", help="Tiempo necesario en minutos")
    disponible = fields.Boolean(string="Disponible", default=True, help="Indica si el plato está disponible")
    categoria = fields.Selection([
        ('entrante', 'Entrante'),
        ('principal', 'Plato principal'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida')
    ], string="Categoría", required=True, help="Tipo de plato")

    # Many2one → Plato pertenece a un Menú
    menu = fields.Many2one(
        "gestion_restaurante_marcos.menu",
        string="Menú",
        ondelete="set null",
        help="Menú al que pertenece este plato"
    )

    # Many2many → Plato tiene Ingredientes
    rel_ingredientes = fields.Many2many(
        "gestion_restaurante_marcos.ingrediente",
        "plato_ingrediente_rel",
        "plato_id",
        "ingrediente_id",
        string="Ingredientes",
        help="Ingredientes del plato"
    )


class Menu(models.Model):
    _name = "gestion_restaurante_marcos.menu"
    _description = "Menú"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre del menú")
    descripcion = fields.Text(string="Descripción", help="Descripción del menú")
    fecha_inicio = fields.Date(string="Fecha inicio", required=True, help="Fecha de inicio del menú")
    fecha_fin = fields.Date(string="Fecha fin", help="Fecha de fin del menú")
    activo = fields.Boolean(string="Activo", default=True, help="Indica si el menú está disponible")

    # One2many → Menú tiene varios Platos
    platos = fields.One2many(
        "gestion_restaurante_marcos.plato",
        "menu",
        string="Platos del menú"
    )


class Ingrediente(models.Model):
    _name = "gestion_restaurante_marcos.ingrediente"
    _description = "Ingrediente"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre del ingrediente")
    es_alergeno = fields.Boolean(string="Es alérgeno", help="Indica si es un ingrediente alérgeno")
    descripcion = fields.Text(string="Descripción", help="Descripción del ingrediente")

    # Many2many inversa
    platos = fields.Many2many(
        "gestion_restaurante_marcos.plato",
        "plato_ingrediente_rel",
        "ingrediente_id",
        "plato_id",
        string="Platos"
    )
