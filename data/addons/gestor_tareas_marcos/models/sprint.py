from odoo import models, fields

class Sprint(models.Model):
    _name = 'gestor_tareas_marcos.sprint'
    _description = 'Sprint'

    nombre = fields.Char(
        string='Nombre del sprint',
        required=True
    )

    fecha_inicio = fields.Date(
        string='Fecha inicio',
        required=True
    )

    fecha_fin = fields.Date(
        string='Fecha fin',
        required=True
    )

    tarea_ids = fields.One2many(
        'gestor_tareas_marcos.task',
        'sprint_id',
        string='Tareas'
    )
