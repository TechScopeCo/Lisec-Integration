
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    item_type =  fields.Char(string='Item Type',)

    
