from odoo import models,fields,api

class StockFleetCategory(models.Model):
    _inherit = "fleet.vehicle.model.category"
    _description = "Define Max Weight and Max Volume for Fleet Category"

    max_weight = fields.Float(string="Max Weight (Kg)")
    max_volume = fields.Float(string="Max Volume (m³)")

    @api.depends('name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.max_weight}kg, {rec.max_volume}m³)"