
# -*- coding: utf-8 -*-
{
    'name': "ISO Code",

    'summary': "This is a custom ISO code",

    'description': """Scope of this module to fulfill the necessary features related to common ISO code form.""",

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','cm_tank_tcode'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_iso_code_view.xml',
        'wizard/cm_iso_code_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_iso_code/static/src/views/*.js',
            'cm_iso_code/static/src/**/*.xml',
            'cm_iso_code/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
