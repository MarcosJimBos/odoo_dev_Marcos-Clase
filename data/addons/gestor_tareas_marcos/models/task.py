from odoo import models, fields

class Task(models.Model):
    _name = 'gestor_tareas_marcos.task'
    _description = 'Tarea'

    nombre = fields.Char(
        string='Nombre',
        required=True
    )

    descripcion = fields.Text(
        string='Descripción'
    )

    fecha_inicio = fields.Date(
        string='Fecha inicio'
    )

    fecha_fin = fields.Date(
        string='Fecha fin'
    )

    sprint_id = fields.Many2one(
        'gestor_tareas_marcos.sprint',
        string='Sprint'
    )
