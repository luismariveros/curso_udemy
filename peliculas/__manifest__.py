# -*- coding:utf-8 -*-

{
    'name': 'Modulo de Peliculas',
    'version': '1.0',
    'depends': ['contacts', 'mail'],
    'author': 'Neurona',
    'website': 'https://www.neurona.com.py',
    'summary': 'Modulos para hacer presupuestos',
    'category': 'Peliculas',
    'description': '''
    Modulo para hacer presupuesto de peliculas
    ''',
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/category.xml",
        "data/secuencia.xml",
        "views/menu.xml",
        "views/genero_views.xml",
        "views/presupuesto_views.xml",
        "wizard/update_wizard_views.xml",
        "report/reporte.xml"
    ],
}
