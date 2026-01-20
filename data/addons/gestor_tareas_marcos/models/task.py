import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


# ==================================================
# MODELO: TAREA
# ==================================================
class Task(models.Model):
    _name = 'gestor_tareas_marcos.task'
    _description = 'Tarea'
    _order = 'fecha_inicio asc'

    codigo = fields.Char(
        string='Código',
        required=True
    )

    nombre = fields.Char(
        string='Nombre',
        required=True
    )

    descripcion = fields.Text(
        string='Descripción'
    )

    fecha_inicio = fields.Date(
        string='Fecha inicio',
        required=True
    )

    fecha_fin = fields.Date(
        string='Fecha fin',
        required=True
    )

    sprint_id = fields.Many2one(
        'gestor_tareas_marcos.sprint',
        string='Sprint',
        ondelete='set null'
    )

    proyecto_id = fields.Many2one(
        'gestor_tareas_marcos.proyectos_marcos',
        string='Proyecto',
        related='sprint_id.proyecto_id',
        store=True,
        readonly=True
    )


    historia_id = fields.Many2one(
        'gestor_tareas_marcos.historia_marcos',
        string='Historia de Usuario',
        ondelete='set null',
        help='Historia de usuario a la que pertenece la tarea'
    )

    estado = fields.Selection(
        [
            ('pendiente', 'Pendiente'),
            ('en_progreso', 'En progreso'),
            ('hecha', 'Hecha')
        ],
        string='Estado',
        default='pendiente',
        required=True
    )

    # ==================================================
    # CONSTRAINS
    # ==================================================
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for tarea in self:
            if tarea.fecha_inicio and tarea.fecha_fin:
                if tarea.fecha_inicio > tarea.fecha_fin:
                    raise ValidationError(
                        'La fecha de inicio no puede ser posterior a la fecha de fin.'
                    )

    # ==================================================
    # LOGS
    # ==================================================
    @api.model
    def create(self, vals):
        _logger.info("📝 Creando tarea [%s]: %s", vals.get('codigo'), vals.get('nombre'))
        return super().create(vals)

    def unlink(self):
        for rec in self:
            _logger.info("🗑️ Eliminando tarea [%s]: %s", rec.codigo, rec.nombre)
        return super().unlink()


# ==================================================
# MODELO: SPRINT
# ==================================================
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

    proyecto_id = fields.Many2one(
        'gestor_tareas_marcos.proyectos_marcos',
        string='Proyecto',
        ondelete='set null'
    )

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for sprint in self:
            if sprint.fecha_inicio and sprint.fecha_fin:
                if sprint.fecha_inicio > sprint.fecha_fin:
                    raise ValidationError(
                        'La fecha de inicio no puede ser posterior a la fecha de fin.'
                    )

    @api.model
    def create(self, vals):
        _logger.info("🏁 Creando sprint: %s", vals.get('nombre'))
        return super().create(vals)

    def unlink(self):
        for rec in self:
            _logger.info("🗑️ Eliminando sprint: %s", rec.nombre)
        return super().unlink()


# ==================================================
# MODELO: PROYECTO
# ==================================================
class ProyectosMarcos(models.Model):
    _name = 'gestor_tareas_marcos.proyectos_marcos'
    _description = 'Proyecto'

    name = fields.Char(
        string='Nombre',
        required=True
    )

    descripcion = fields.Text(
        string='Descripción'
    )

    sprint_ids = fields.One2many(
        'gestor_tareas_marcos.sprint',
        'proyecto_id',
        string='Sprints'
    )

    historia_ids = fields.One2many(
        'gestor_tareas_marcos.historia_marcos',
        'proyecto_id',
        string='Historias de usuario'
    )


# ==================================================
# MODELO: HISTORIA DE USUARIO
# ==================================================
class HistoriaMarcos(models.Model):
    _name = 'gestor_tareas_marcos.historia_marcos'
    _description = 'Historia de Usuario'

    name = fields.Char(
        string='Nombre',
        required=True
    )

    descripcion = fields.Text(
        string='Descripción'
    )

    proyecto_id = fields.Many2one(
        'gestor_tareas_marcos.proyectos_marcos',
        string='Proyecto',
        ondelete='set null'
    )

    tarea_ids = fields.One2many(
        'gestor_tareas_marcos.task',
        'historia_id',
        string='Tareas'
    )
