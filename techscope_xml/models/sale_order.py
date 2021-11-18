
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    total_weight =  fields.Float(string='Order Total Weight',)
    total_sqm =  fields.Float(string='Order Total SQM',)
    total_qty =  fields.Float(string='Order Total QTY',)
    order_number =  fields.Char(string='Customer Order Number',)
    project_number =  fields.Char(string='Project Number',)
    project_name =  fields.Char(string='Project Name',)
    delivery_type =  fields.Char(string='Delivery Type',)
    delivery_date = fields.Date(string='Delivery Date',)
    order_create_user = fields.Many2one(
        string='Create User',
        comodel_name='res.users',
    )
    

    
    
