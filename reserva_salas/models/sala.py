# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Sala(models.Model):
    #Modelo representativo de las salas de reuniones
    _name = 'reserva.sala'  # Nombre técnico modelo en la BD
    _description = 'Sala de Reuniones'  # Descripción legible
    _order = 'name'  # Ordenar por nombre por defecto
    
    # Campos del modelo
    name = fields.Char(
        string='Nombre de la Sala',
        required=True,
        help='Nombre identificativo de la sala'
    )
    
    capacidad = fields.Integer(
        string='Capacidad Máxima',
        required=True,
        help='Número máximo de personas que caben'
    )
    
    equipamiento = fields.Text(
        string='Equipamiento Disponible',
        help='Descripción del equipamiento: proyector, pizarra, etc.'
    )

    # Relación con reservas
    reserva_ids = fields.One2many(
        'reserva.reserva',
        'sala_id',
        string='Reservas'
    )
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name or 'Sin Nombre'} (Cap: {record.capacidad or 0})"
            result.append((record.id, name))
        return result