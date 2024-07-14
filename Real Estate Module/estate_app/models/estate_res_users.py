from odoo import models,fields

class EstatePropertyUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property', 'salesperson_id',
        string="Properties",
        help="Properties linked to this salesperson",
        domain= ['|',('state','in',['new']),('state','in',['offer received']),]
    )
