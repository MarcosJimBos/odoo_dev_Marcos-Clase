{
    'name': 'Gestión Restaurante Marcos',
    'version': '1.0',
    'author': 'Marcos',
    'depends': ['base'],
    'application': True,
    'installable': True,
    'summary': 'Gestión de platos, menús e ingredientes para restaurante',
    'description': """
Módulo de gestión de restaurante de Marcos.
Incluye:
- Modelo Plato
- Modelo Menú
- Modelo Ingrediente
- Relaciones many2one, one2many y many2many
- Vistas, menús y permisos
""",
    'data': [
        'security/ir.model.access.csv',
        'views/plato_views.xml',
        'views/menu_views.xml',
        'views/ingrediente_views.xml',
        'views/menu_items.xml',
    ],
}
