from odoo import models,fields,api,exceptions, _
from odoo.tools import is_html_empty
from odoo.exceptions import ValidationError,UserError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import datetime 
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _rec_name = "name"
    _order = "id desc"
    _inherit = ["mail.thread","mail.activity.mixin"]


    name = fields.Char(required=True, string="Property Name")
    description = fields.Text(string="Description")
    pincode = fields.Char(string="Pincode/Postcode")
    date_availability = fields.Date(
        copy=False,
        default=datetime.now() + relativedelta(months=3),
        string="Available From"
        )
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default='2', string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        help="Select Garden Orientation"
    )
    active = fields.Boolean(string='Active',default=True)
    state = fields.Selection(
        selection=[
            ('new','New'),
            ('offer received','Offer Received'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancel','Canceled')
        ],
        required=True,
        copy=False,
        tracking=True,
        default='new',
        string="Status"
    )
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, readonly=True, tracking=True,)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers", tracking=True,)
    total_area = fields.Integer(compute="_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_best_price", string="Best Offer", tracking=True,)
    image_property = fields.Image(store=True)

    # SQL Constraints to Check Expected and Selling Price are Positive
    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price >= 0)',
         "A Property's Expected Price Must be Positive!"),
        ('positive_selling_price', 'CHECK(selling_price >= 0)',
         "A Property's Selling Price Must be Positive!"),
    ]

    # Python Constrain to Ensure Selling Price Can't be Lower then 90% Expected Price 
    @api.constrains('selling_price', 'expected_price')
    def check_price(self):
        for price in self:
            if float_compare(price.selling_price, 0.9 * price.expected_price, 0) == -1 and price.buyer_id:
                raise ValidationError("Selling Price cannot be lower than 90% of the Expected Price")

            # if price.selling_price <= 0.9 * price.expected_price and price.buyer_id:
            #     raise ValidationError("Selling Price cannot be lower than 90% of the Expected Price")

    # Total Area Compute Field
    @api.depends('living_area', 'garden_area')
    def _total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    # Best Selling Price = Maximum Offer Price
    @api.depends('offer_ids.price',)
    def _best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'),default=0)

    # If Garden is Checked, Automatic Garder Area & Orientation Set
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # Give non-blocking Warning When User Did not Entered Pincode
    @api.onchange('name')
    def _onchange_pincode(self):
        if self.pincode == False and self.name:
            return {'warning': {
                'title': ("Notice"),
                'message': ("Don't Forget to Entered the Pincode!!")}}

    # Sold & Cancel Button for Property 
    def sold_action(self):
        for property in self:
            if property.state == 'cancel':
                raise exceptions.UserError("Canceled Properties Can't Be Sold")
            elif property.state == 'offer accepted':
                # Update property state
                property.state = 'sold'
            else:
                raise exceptions.UserError("Invalid Property State for Selling")
        return True
    
    def cancel_action(self):
        for property in self:
            if property.state == 'sold':
                raise exceptions.UserError("Sold Properties Can't Be Canceled")
            else:
                property.state = 'cancel'
        return True

    # Can't delete sold, offer received or accpeted properties!
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_not_new_or_canceled(self):
        if self.state == 'sold' or self.state == 'offer received' or self.state == 'offer accepted':
            raise UserError("Only New and Canceled Properties Can Be Deleted!")

    # If Property is 'Canceled', then all offers will be deleted!
    @api.model
    def write(self, vals):
        if 'state' in vals and vals['state'] == 'cancel':
            self.offer_ids.unlink() # Delete all offers associated with the property

        return super(EstateProperty, self).write(vals)