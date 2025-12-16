from odoo import models, fields

class Task(models.Model):
    _name = 'gestor_tareas_marcos.task'
    _description = 'Tarea'

    nombre = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la tarea'
    )

    descripcion = fields.Text(
        string='Descripción',
        help='Descripción de la tarea'
    )
