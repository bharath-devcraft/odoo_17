import base64
from collections import OrderedDict
from datetime import datetime
import json
from odoo import http
import uuid

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, Response
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


def validate_access_token(func):
    def wrapper(*args, **kwargs):
        kwargs = json.loads(http.request.httprequest.data)
        
        access_token = request.httprequest.headers.get("Authorization") 
        if not access_token:
            return {'status':401,'message':'Missing Access Token'}
        
        user_id = http.request.httprequest.headers.get('user_id')
        access_token = http.request.httprequest.headers.get('access_token')
        print(access_token,"EEEEEEEEEEEEE",kwargs)
        
        # Add your token validation logic here
        if user_id and access_token:
            # Perform token validation based on user ID and access token
            # Return True if valid, False if invalid
            return True
        else:
            return False

    return wrapper
class TravelManagement(http.Controller):
    @http.route('/travel_management/travel_management', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/travel_management/travel_management/objects/<model("travel_management.travel_management"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('travel_management.object', {
            'object': obj
        })

    @http.route('/travel_management/post_bank_api', type='json', auth='public', methods=['POST'], csrf=False)
    @validate_access_token
    def create_bank(self, **post):
        bank = http.request.env['organizer_bank_details.organizer_bank_details']
        post = json.loads(http.request.httprequest.data)
        if post:
            bank = bank.create({
                'org_account_no': post.get('org_account_no'),
                'org_account_holder_name': post.get('org_account_holder_name'),
                'org_bank': int(post.get('org_bank')),
                'org_branch_name': int(post.get('org_branch_name')),
                'org_bank_ifsc_code': int(post.get('org_bank_ifsc_code')),
                'org_upi_id': int(post.get('org_upi_id')),
            })
            return {'message': 'Bank created successfully', 'bank_id': bank.id}
        else:
            return {'message': 'No data received for creating a bank record'}


class CustomerPortal(portal.CustomerPortal):
    @http.route(['/my/travel_booking', '/my/travel_booking/page/<int:page>'], type='http', auth="user", website=True)
    def portal_travel_bookings(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        return self._render_travel_portal(
            "travel_management.portal_travel_bookings",
            page, date_begin, date_end, sortby, filterby,
            [],
            {
                'all': {'label': _('All'), 'domain': [('state', 'in', ['draft', 'confirmed', 'validate', 'payment_request','payment_received','approved','reject','wf_cancel','cancel','closed'])]},
                'Booked': {'label': _('Booked'), 'domain': [('state', '=', 'approved')]},
                'cancel': {'label': _('Cancelled'), 'domain': [('state', 'in', ['wf_cancel','cancel'])]},
                'Closed': {'label': _('Closed'), 'domain': [('state', '=', 'closed')]},
            },
            'all',
            "/my/travel_booking",
            'my_travel_history',
            'Travel Management',
            'bookings'
        )
    
    def _get_travel_searchbar_sortings(self):
        return {
            'date': {'label': _('Newest'), 'order': 'crt_date desc, id desc'},
            'name': {'label': _('Name'), 'order': 'name asc, id asc'},
            'amount_total': {'label': _('Total Amount'), 'order': 'total_amount desc, id desc'},
        }

    def _render_travel_portal(self, template, page, date_begin, date_end, sortby, filterby, domain, searchbar_filters, default_filter, url, history, page_name, key):
        values = self._prepare_portal_layout_values()
        TravelManagement = request.env['travel_management.travel_management']

        if date_begin and date_end:
            domain += [('crt_date', '>', date_begin), ('crt_date', '<=', date_end)]

        searchbar_sortings = self._get_travel_searchbar_sortings()
        # default sort

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        
        if searchbar_filters:
            # default filter
            if not filterby:
                filterby = default_filter
            domain += searchbar_filters[filterby]['domain']

        # count for pager
        count = TravelManagement.search_count(domain)

        # make pager
        pager = portal_pager(
            url=url,
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=count,
            page=page,
            step=self._items_per_page
        )

        # search the travel bookings to display, according to the pager data
        bookings = TravelManagement.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session[history] = bookings.ids[:100]

        values.update({
            'date': date_begin,
            key: bookings,
            'page_name': page_name,
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': url,
        })

        return request.render(template, values)

class TokenAuthController(http.Controller):
    ACCESS_TOKENS = {}

    @http.route('/generate_access_token', type='json', auth='public', methods=['POST'], csrf=False)
    def generate_access_token(self, **post):
        post = json.loads(http.request.httprequest.data)
        user_id = post.get('user_id')
        if user_id:
            access_token = str(uuid.uuid4())
            self.ACCESS_TOKENS[user_id] = access_token
            return {'access_token': access_token}
        else:
            return {'error': 'User ID not provided'}

