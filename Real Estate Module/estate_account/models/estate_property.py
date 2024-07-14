from odoo import fields, models, exceptions,Command
from datetime import date

class EstateAccount(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        for property in self:
            # Create invoice
            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_payment_term_id': None,
                'invoice_line_ids': [
                    Command.create({
                        'name': f'{property.name} Commission',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })
            return super().sold_action()
