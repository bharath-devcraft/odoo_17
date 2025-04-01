
# -*- coding: utf-8 -*-
{
    'name': "Port Product Group",

    'summary': "This is a custom port product group",

    'description': """Scope of this module to fulfill the necessary features related to common port product group form.""",

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_port_product_group_view.xml',
        'wizard/cm_port_product_group_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_port_product_group/static/src/views/*.js',
            'cm_port_product_group/static/src/**/*.xml',
            'cm_port_product_group/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
