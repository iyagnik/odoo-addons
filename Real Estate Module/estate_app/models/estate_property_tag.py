from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _rec_name = "tag"
    _order = "tag"

    tag = fields.Char(required=True, string="Property Tag")
    color = fields.Integer()

    # SQL Contraint for Unique Property Tags
    _sql_constraints = [
        ('tag_uniq', "unique(tag)", 
         "Property Tag Must Not Be Same!")
    ]
