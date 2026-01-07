import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)

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

    def create(self, vals):
        _logger.info("Creando tarea: %s", vals.get('nombre'))
        return super().create(vals)

    def write(self, vals):
        _logger.info("Modificando tarea: %s", self.nombre)
        return super().write(vals)

    def unlink(self):
        for rec in self:
            _logger.info("Eliminando tarea: %s", rec.nombre)
        return super().unlink()
