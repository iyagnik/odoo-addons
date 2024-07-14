from odoo import models, fields, api

class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Estate Property Offer Wizard'

    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_ids = fields.Many2many('estate.property', string='Properties', required=True)

    def show_offer_list(self):
        partner = self.partner_id
        properties = self.property_ids
        if partner and properties:
            offers = self.env['estate.property.offer'].search([
                ('property_id', 'in', properties.ids),
                ('partner_id', '=', partner.id)
            ])
            action = {
                'name': 'Offer List',
                'view_mode': 'tree,form',
                'res_model': 'estate.property.offer',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', offers.ids)],
                'context': {'default_partner_id': partner.id},
                'help': '<p class="o_view_nocontent_neutral_face">No Offers Found! 😐</p>',
            }

            if len(offers) == 1:
                action['view_mode'] = 'form'
                action['res_id'] = offers.id

            return action
        return True

    def show_offer_list_btn(self):
        return True