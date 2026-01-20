{
    'name': 'Gestión Restaurante Marcos',
    'version': '1.0',
    'author': 'Marcos',
    'category': 'Services/Restaurant',
    'summary': 'Gestión de platos, menús, ingredientes, categorías y chefs',
    'description': """
Módulo de gestión de restaurante de Marcos.

Incluye:
- Modelo Plato
- Modelo Menú
- Modelo Ingrediente
- Modelo Categoría
- Modelo Chef
- Relaciones many2one, one2many y many2many
- Vistas, menús y permisos
""",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_items.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
}

