"""User"""
import time
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CmGroups(models.Model):
	"""User"""
	_name = "res.groups"
	_inherit = "res.groups"
	_description = "User Groups"	
	
	custom_group = fields.Boolean('Custom Group')	
		
	
