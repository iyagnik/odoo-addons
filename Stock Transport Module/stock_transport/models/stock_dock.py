from odoo import models,fields
class StockFleet(models.Model):
    _name = "stock.dock"

    name = fields.Char()