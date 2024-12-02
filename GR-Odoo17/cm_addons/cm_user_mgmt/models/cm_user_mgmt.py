# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, tools, api, _
from odoo.exceptions import UserError

RES_USERS = 'res.users'
CM_MASTER = 'cm.master'


CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmUserMgmt(models.Model):
    """User"""
    _name = "res.users"
    _inherit = ['res.users','mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _description = "User Managment"

    
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", tracking=True, readonly=True) 
    copy_user_id = fields.Many2one(RES_USERS, string="Existing User", copy=False, domain=[('status', '=', 'active')])
    user_menu_ids = fields.Many2many(
        'ir.ui.menu',
        'ir_ui_menu_user_rel',
        'user_id',
        'menu_id',
        'Access Menu',domain=[('name','!=','')], ondelete='restrict', c_rule=True)
    groups_ids = fields.Many2many(
        'res.groups',
        'res_groups_users_rel',
        'uid',
        'gid',
        'Groups', ondelete='restrict', c_rule=True)       
        
    
    access_company_ids = fields.Many2many(
        'res.company',
        'user_company_mapping',
        'user_id',
        'company_id',
        store=True,
        string='Access Companies', ondelete='restrict', c_rule=True)
    division_ids = fields.Many2many(
        'res.company',
        'user_division_mapping',
        'user_id',
        'division_id',
        store=True,
        string='Access Divisions', ondelete='restrict', c_rule=True)
        
    department_ids = fields.Many2many(
        'res.company',
        'user_department_mapping',
        'user_id',
        'department_id',
        store=True,
        string='Access Departments', ondelete='restrict', c_rule=True)
 
    mobile_no = fields.Char(string="Mobile No", size=15)
    ext_no = fields.Char(string="Ext No", copy=False, size=15)    
    sign_img = fields.Image(string="Signature Image", copy=False, max_height=128, max_width=128)   
    division_id = fields.Many2one(CM_MASTER, string="Division", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    department_id = fields.Many2one(CM_MASTER, string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    fiscal_year_id = fields.Many2one('cm.fiscal.year',string="Fiscal Year", copy=False)
    
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    note = fields.Html(string="Notes", copy=False, sanitize=False)

    #Entry info
    active = fields.Boolean(string="Visible", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", tracking=True, readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    inactive_date = fields.Datetime(string="Inactivated Date", copy=False, readonly=True)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)

    
    #constrains
    @api.constrains('name','login')
    def name_validation(self):
        """ name_validation """
        if self.login:
            if is_special_char(self.env, self.login):
                raise UserError(_('Special character is not allowed in login field'))
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_('Special character is not allowed in Display Name field'))            
        return True
    
    
    @validation    
    def entry_approve(self):
        """ entry_approve """
        if self.status in ('draft','editable'):
            self.write({'status': 'active',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
        return True

    def entry_draft(self):
        """ entry_draft """
        self.write({'status': 'editable'})
        return True

    def entry_inactive(self):
        """ entry_inactive """
        if self.status == 'active':
            if self.inactive_remark:
                if self.inactive_remark.strip():
                    if len(self.inactive_remark.strip())>= 10:
                        self.write({'status':'inactive',
                                    'active':False,
                                    'inactive_user_id': self.env.user.id,
                                    'inactive_date': time.strftime('%Y-%m-%d %H:%M:%S')})
                    else:
                        raise UserError(
                            _('Minimum 10 characters are required for Inactive Remarks.'))
            else:
                raise UserError(
                    _('Inactive remark is must !!, Enter the remarks in Inactive Remark field.'))
        else:
            raise UserError(
                    _('Unable to inactive other than active entry.'))
    
    
    

    def copy_user_menus(self):
        """Copy User"""
        self.env.cr.execute(
            """delete from ir_ui_menu_user_rel where user_id=%d""" %
            self.id)
        self.env.cr.execute(
            """delete from res_groups_users_rel where uid=%d""" %
            self.id)
        self.env.cr.execute(
            """select * from ir_ui_menu_user_rel where user_id=%d""" %
            self.copy_user_id.id)
        data = self.env.cr.dictfetchall()
        for i in data:
            self.env.cr.execute(
                """insert into ir_ui_menu_user_rel values(%s,%s)""" %
                (self.id, i['menu_id']))
        self.env.cr.execute(
            """select * from res_groups_users_rel where uid=%d""" %
            self.copy_user_id.id)
        data1 = self.env.cr.dictfetchall()
        for j in data1:
            self.env.cr.execute(
                """insert into res_groups_users_rel values(%s,%s)""" %
                (j['gid'], self.id))
        return True
        
    def unlink(self):
        """ Unlink """
        for rec in self:
            if rec.status not in ('draft') or rec.entry_mode == 'auto':
                raise UserError("You can't delete other than manually created draft entries.")
            if rec.status in ('draft'):
                res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.del_draft_entry')
                is_mgmt = self.env['res.users'].has_group('cm_user_mgmt.group_mgmt_admin')
                if not res_config_rule and self.user_id != self.env.user and not(is_mgmt):
                    raise UserError("You can't delete other users draft entries")
                models.Model.unlink(rec)
        return True
    
    def write(self, vals):
        """ write """       
        vals.update({'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'update_user_id': self.env.user.id})
        self.self.clear_caches()
        return super(CmUserMgmt, self).write(vals)
        
    @api.model
    def retrieve_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the transaction views.
        """

        result = {
            'all_draft': 0,
            'all_active': 0,
            'all_inactive': 0,
            'all_editable': 0,
            'my_draft': 0,
            'my_active': 0,
            'my_inactive': 0,
            'my_editable': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0,
        }
        
        
        #counts
        cm_user = self.env['res.users']
        result['all_draft'] = cm_user.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_user.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_user.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_user.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_user.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_user.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_user.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_user.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_user.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_user.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_user.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_user.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result   
        
    


class Menu(models.Model):
	_inherit = 'ir.ui.menu'

	@api.model
	@tools.ormcache_context('self._uid', 'debug', keys=('lang',))
	def load_menus(self, debug):
		""" Loads all menu items (all applications and their sub-menus).

		:return: the menu root
		:rtype: dict('children': menu_nodes)
		"""
		fields = ['name', 'sequence', 'parent_id', 'action', 'web_icon']
		menu_roots = self.get_user_roots()
		menus_ids = self.env['res.users'].browse(self.env.user.id).user_menu_ids
		
		root_menu=[]
		total_menu=[]
		
		#### Added by Karthikeyan Starts
		for c in menus_ids:
			if not c.parent_id:
				root_menu.append(c.id)
			total_menu.append(c.id)
		if self.env.user.id not in (1,2,3):
			menu_roots=self.browse(root_menu)
		#### Added by Karthikeyan Ends
		
		menu_roots_data = menu_roots.read(fields) if menu_roots else []
		menu_root = {
			
			
			'id': False,
			'name': 'root',
			'parent_id': [-1, ''],
			'children': [menu['id'] for menu in menu_roots_data],
			'all_menu_ids': menu_roots.ids,
			
		}

		all_menus = {'root': menu_root}

		if not menu_roots_data:
			return all_menus

		# menus are loaded fully unlike a regular tree view, cause there are a
		# limited number of items (752 when all 6.1 addons are installed)
		menus_domain = [('id', 'child_of', menu_roots.ids)]
		
		
		#### Added by Karthikeyan Starts
		if self.env.user.id not in (1,2,3):
			menus=self.browse(total_menu)
			#### Added by Karthikeyan Ends
			
			menu_items = menus.read(fields)
		else:
		
			blacklisted_menu_ids = self._load_menus_blacklist()
			if blacklisted_menu_ids:
				menus_domain = expression.AND([menus_domain, [('id', 'not in', blacklisted_menu_ids)]])
			menus = self.search(menus_domain)
			menu_items = menus.read(fields)
		xmlids = (menu_roots + menus)._get_menuitems_xmlids()

		# add roots at the end of the sequence, so that they will overwrite
		# equivalent menu items from full menu read when put into id:item
		# mapping, resulting in children being correctly set on the roots.
		menu_items.extend(menu_roots_data)

		mi_attachments = self.env['ir.attachment'].sudo().search_read(
			domain=[('res_model', '=', 'ir.ui.menu'),
					('res_id', 'in', [menu_item['id'] for menu_item in menu_items if menu_item['id']]),
					('res_field', '=', 'web_icon_data')],
			fields=['res_id', 'datas', 'mimetype'])

		mi_attachment_by_res_id = {attachment['res_id']: attachment for attachment in mi_attachments}

		# set children ids and xmlids
		menu_items_map = {menu_item["id"]: menu_item for menu_item in menu_items}
		for menu_item in menu_items:
			menu_item.setdefault('children', [])
			parent = menu_item['parent_id'] and menu_item['parent_id'][0]
			menu_item['xmlid'] = xmlids.get(menu_item['id'], "")
			if parent in menu_items_map:
				menu_items_map[parent].setdefault(
					'children', []).append(menu_item['id'])
			attachment = mi_attachment_by_res_id.get(menu_item['id'])
			if attachment:
				menu_item['web_icon_data'] = attachment['datas']
				menu_item['web_icon_data_mimetype'] = attachment['mimetype']
			else:
				menu_item['web_icon_data'] = False
				menu_item['web_icon_data_mimetype'] = False
		all_menus.update(menu_items_map)

		# sort by sequence
		for menu_id in all_menus:
			all_menus[menu_id]['children'].sort(key=lambda id: all_menus[id]['sequence'])

		# recursively set app ids to related children
		def _set_app_id(app_id, menu):
			menu['app_id'] = app_id
			for child_id in menu['children']:
				_set_app_id(app_id, all_menus[child_id])

		for app in menu_roots_data:
			app_id = app['id']
			_set_app_id(app_id, all_menus[app_id])

		# filter out menus not related to an app (+ keep root menu)
		all_menus = {menu['id']: menu for menu in all_menus.values() if menu.get('app_id')}
		all_menus['root'] = menu_root

		return all_menus
