# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Reserva(models.Model):
    #Modelo representativo de las reservas de salas
    _name = 'reserva.reserva'
    _description = 'Reserva de Sala'
    _order = 'fecha_reserva desc, hora_inicio'  # Ordenado por fecha descendente

    # Relación con la sala
    sala_id = fields.Many2one(
        'reserva.sala',  # Modelo relacionado
        string='Sala',
        required=True,
        help='Sala que se está reservando'
    )
    
    # Campo fecha y hora
    fecha_reserva = fields.Date(
        string='Fecha de Reserva',
        required=True,
        default=fields.Date.context_today,  # Por defecto hoy
        help='Fecha para la cual se hace la reserva'
    )
    
    hora_inicio = fields.Datetime(
        string='Hora de Inicio',
        required=True,
        help='Momento exacto de inicio de la reserva'
    )
    
    hora_fin = fields.Datetime(
        string='Hora de Finalización',
        required=True,
        help='Momento exacto de fin de la reserva'
    )
    
    #Para quién es la reserva
    usuario_id = fields.Many2one(
        'res.users',
        string='Usuario Reserva',
        required=True,
        domain=[('login', 'ilike', '@reservas.cl')],
        help='Seleccione el usuario que hara la reserva'
    )
    
    # Campo opcional de comentarios
    comentarios = fields.Text(
        string='Comentarios',
        help='Información adicional sobre la reserva'
    )
    
    # Campo computado para duración de reserva
    duracion_horas = fields.Float(
        string='Duración (Horas)',
        compute='_compute_duracion',
        store=True,
        help='Duración calculada de la reserva'
    )
    
    # Campo para el estado de la reserva
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ], string='Estado', default='confirmada')
    
    #Relación con invitaciones
    invitacion_ids = fields.One2many(
        'reserva.invitacion',
        'reserva_id', 
        string='Invitaciones',
        help='Invitaciones asociadas a esta reserva'
    )

    @api.depends('hora_inicio', 'hora_fin')
    def _compute_duracion(self):
        #Duración de inicio y fin
        for record in self:
            if record.hora_inicio and record.hora_fin:
                delta = record.hora_fin - record.hora_inicio
                record.duracion_horas = delta.total_seconds() / 3600.0
            else:
                record.duracion_horas = 0.0
    
    @api.constrains('hora_inicio', 'hora_fin')
    def _check_fechas_validas(self):
        #Valida que la hora final sea posterior a la inicial
        for record in self:
            if record.hora_inicio and record.hora_fin:
                if record.hora_fin <= record.hora_inicio:
                    raise ValidationError(
                        '❌ Error: La hora de finalización debe ser POSTERIOR a la hora de inicio.'
                    )
    
    @api.constrains('usuario_id')
    def _check_email_dominio(self):
        #Valida que usuario tenga email @reservas.cl
        for record in self:
            if record.usuario_id:
                email = record.usuario_id.email or record.usuario_id.login or ''
                if '@reservas.cl' not in email:
                    raise ValidationError(
                        f"Solo se permiten usuarios con email @reservas.cl. "
                        f"El usuario {record.usuario_id.name} tiene: {email or 'Sin email'}"
                    )
    
    @api.onchange('usuario_id')
    def _onchange_usuario_id(self):
        #Advertencia al seleccionar usuario sin email @reservas.cl
        if self.usuario_id:
            email = self.usuario_id.email or self.usuario_id.login or ''
            if '@reservas.cl' not in email:
                return {
                    'warning': {
                        'title': 'Usuario no válido',
                        'message': 'Solo se permiten usuarios con email @reservas.cl.'
                    }
                }
    
    @api.model
    def create(self, vals):
        # Validar email del usuario antes de crear
        if 'usuario_id' in vals:
            usuario = self.env['res.users'].browse(vals['usuario_id'])
            email = usuario.email or usuario.login or ''
            if '@reservas.cl' not in email:
                raise ValidationError('Solo usuarios con email @reservas.cl pueden crear reservas')
        
        # Crear la reserva (llamado al método original)
        nueva_reserva = super(Reserva, self).create(vals)
        
        return nueva_reserva
    
    def write(self, vals):
        # Validar email si se cambia el usuario
        if 'usuario_id' in vals:
            usuario = self.env['res.users'].browse(vals['usuario_id'])
            email = usuario.email or usuario.login or ''
            if '@reservas.cl' not in email:
                raise ValidationError('Solo usuarios con email @reservas.cl')
        
        # Actualizar la reserva (llamar método original)
        return super(Reserva, self).write(vals)
    
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sala_id.name or 'Sin Sala'} - {record.fecha_reserva or 'Sin Fecha'}"
            result.append((record.id, name))
        return result