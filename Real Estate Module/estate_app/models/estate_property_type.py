from odoo import models,fields,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _rec_name = "type"
    _order = "type"

    type = fields.Char(required=True, string="Property Type")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer('Sequence' ,help="Used to manually order properties types.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    # SQL Contraint for Unique Property Types
    _sql_constraints = [
        ('type_uniq', "unique(type)", 
         "Property Type Must Not Be Same!")
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
