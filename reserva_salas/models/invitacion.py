# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Invitacion(models.Model):
    _name = 'reserva.invitacion'
    _description = 'Invitación a Reserva de Sala'
    _order = 'fecha_invitacion desc'
    
    # Relación con la reserva
    reserva_id = fields.Many2one(
        'reserva.reserva',
        string='Reserva',
        required=True,
        ondelete='cascade'
    )
    
    # Usuario invitado (reservas.cl)
    usuario_invitado_id = fields.Many2one(
        'res.users',
        string='Usuario Invitado',
        required=True,
        domain=[('login', 'ilike', '@reservas.cl')]
    )
    
    fecha_invitacion = fields.Datetime(
        string='Fecha de Invitación',
        default=fields.Datetime.now
    )
    
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada')
    ], string='Estado', default='pendiente')
    
    token_verificacion = fields.Char(string='Token de Verificación', copy=False)
    
    #EJEMPLO: Campo computado
    nombre_invitacion = fields.Char(
        string='Invitación',
        compute='_compute_nombre_invitacion',
        store=True
    )
    
    @api.depends('reserva_id', 'usuario_invitado_id')
    def _compute_nombre_invitacion(self):
        for record in self:
            record.nombre_invitacion = (
                f"Invitación: {record.usuario_invitado_id.name} → "
                f"{record.reserva_id.sala_id.name}"
            )
    
    #EJEMPLO: API Constraints
    @api.constrains('usuario_invitado_id')
    def _check_usuario_valido(self):
        for record in self:
            if (record.usuario_invitado_id and 
                '@reservas.cl' not in (record.usuario_invitado_id.login or '')):
                raise ValidationError('Solo se pueden invitar usuarios con email @reservas.cl')
    
    #EJEMPLO: Método para verificar invitación
    def verificar_invitacion(self, token):
        """Verifica si el token de invitación es válido"""
        self.ensure_one()
        if self.token_verificacion == token:
            self.estado = 'aceptada'
            return True
        return False
    
    @api.model
    def create(self, vals):
        # Generar token único al crear
        import secrets
        if 'token_verificacion' not in vals:
            vals['token_verificacion'] = secrets.token_urlsafe(16)
        
        return super().create(vals)