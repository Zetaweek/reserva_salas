# -*- coding: utf-8 -*-
{
    'name': 'Reserva de Salas',
    'version': '1.0.0',
    'category': 'Productivity',
    'summary': 'Gestión de reservas de salas de reuniones',
    'description':
    """
        Módulo para gestionar reservas de salas de reuniones.
        Incluye sistema de invitaciones y validación de usuarios.
        
        Características:
        * Gestión de salas con capacidad y equipamiento
        * Reservas con fecha, hora y responsable
        * Solo administradores pueden realizar reservas
        * Sistema de comentarios para reservas
    """,
    'author': 'Zetaweek',
    'website': 'https://github.com/Zetaweek',
    'depends': ['base', 'web', 'contacts', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/sala_views.xml',
        'views/reserva_views.xml',
        'views/invitacion_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}