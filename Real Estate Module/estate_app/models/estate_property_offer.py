from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers From Buyer"
    _order = "price desc"
    _rec_name = "property_id"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ],
        copy=False,
        string="Status",
        readonly=True
    )
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', required=True, string="Property")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", related='property_id.property_type_id', store=True)

    # SQL Contraint to ensure Offer Price is Positive
    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price >= 0)',
         "A Property's Offer Price Must be Positive!")
    ]

    # Compute Field for Validity & Date Deadline
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.validity and offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)
                
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                create_date_as_date = offer.create_date.date()
                offer.validity = (offer.date_deadline - create_date_as_date).days

    # Accept and Refused Offer - Action Buttons
    def status_accept(self):
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer accepted'

                # Reject all other offers for the same property
            other_offers = self.search([
                ('property_id', '=', offer.property_id.id), #Get all offers associated with the same property as the current offer.
                ('id', '!=', offer.id),  # Exclude the current offer
            ])
            other_offers.write({'status': 'refused'})

    def status_refused(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.buyer_id = None
            offer.property_id.selling_price = 0

    # At offer creation, state change to 'offer received'
    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            offer = super(EstatePropertyOffer, self).create(vals)
            property_obj = self.env['estate.property'].browse(vals.get('property_id'))
            property_obj.state = 'offer received'

            # Check new offer's price is greater than any existing offer
            existing_offers = self.search([('property_id', '=', vals.get('property_id')),
                                        ('id', '!=', offer.id)])
            for existing_offer in existing_offers:
                if offer.price < existing_offer.price:
                    raise ValidationError("Offer Price should be higher than existing offers.")
            return offer
    
    # Change state to 'new' if delete all offers
    def unlink(self):
        property_ids = self.mapped('property_id')
        result = super(EstatePropertyOffer, self).unlink()
        
        # Check if there are any remaining offers for the associated properties
        for property_id in property_ids:
            remaining_offers = self.search([('property_id', '=', property_id.id)])
            if not remaining_offers:
                property_id.state = 'new'
        return result
