# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime

class Estate(http.Controller):

    @http.route(['/estate/properties', '/estate/properties/page/<int:page>'], auth='public', website=True)
    def property_view(self, page=1, search=None, available_from=None, **kwarg):

        limit = 6

        domain = [('state', 'not in', ['Sold'])]
        if search:
            domain += [('name', 'ilike', search)]

        if available_from:
            try:
                available_from_date = datetime.strptime(available_from, "%Y-%m-%d").date()
                domain += [('date_availability', '>=', available_from_date)]
            except ValueError:
                # Handle invalid date format
                pass

        properties = http.request.env['estate.property']

        total_records = properties.sudo().search_count(domain,)

        pager = http.request.website.pager(url='/estate/properties', total=total_records, page=page, step=limit)

        offset = pager['offset']
        properties = properties[offset: offset + limit]

        data = {
            "properties": properties.search(domain, limit=limit, offset=offset, order="create_date desc"),
            "pager": pager,
            "search": search,
            "available_from": available_from
        }
        response = http.request.render('estate_app.properties', data)

        return response

    @http.route('/estate/properties/<model("estate.property"):name>', auth='public', website=True)
    def property_view_form(self, name):
        data = {
            "property": name
        }
        response = http.request.render('estate_app.object', data)
        return response
