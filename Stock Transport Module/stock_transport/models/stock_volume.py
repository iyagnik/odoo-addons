from odoo import models, fields, api

class StockPickingVolume(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(compute="_compute_volume", store=True)

    @api.depends('move_ids.product_id.volume', 'move_ids.quantity')
    def _compute_volume(self):
        for rec in self:
            rec.volume = sum(line.product_id.volume * line.quantity for line in rec.move_ids)
