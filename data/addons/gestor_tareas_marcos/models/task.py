import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)

class Task(models.Model):
    _name = 'gestor_tareas_marcos.task'
    _description = 'Tarea'

    nombre = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    fecha_inicio = fields.Date(string='Fecha inicio')
    fecha_fin = fields.Date(string='Fecha fin')
    sprint = fields.Char(string='Sprint')

    def create(self, vals):
        _logger.info("🟢 CREANDO TAREA: %s", vals.get('nombre'))
        return super(Task, self).create(vals)

    def write(self, vals):
        _logger.info("🟡 MODIFICANDO TAREA ID %s", self.id)
        return super(Task, self).write(vals)

    def unlink(self):
        for task in self:
            _logger.info("🔴 BORRANDO TAREA: %s", task.nombre)
        return super(Task, self).unlink()
º