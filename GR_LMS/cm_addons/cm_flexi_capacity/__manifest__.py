
# -*- coding: utf-8 -*-
{
    'name': "Flexi Capacity",

    'summary': "This is a custom flexi capacity",

    'description': """Scope of this module to fulfill the necessary features related to common flexi capacity form.""",

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
        'views/cm_flexi_capacity_view.xml',
        'wizard/cm_flexi_capacity_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_flexi_capacity/static/src/views/*.js',
            'cm_flexi_capacity/static/src/**/*.xml',
            'cm_flexi_capacity/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
