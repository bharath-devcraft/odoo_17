
# -*- coding: utf-8 -*-
{
    'name': "Tax Mapping",

    'summary': "This is a custom tax mapping",

    'description': """Scope of this module to fulfill the necessary features related to common tax mapping form.""",

    'author': "Praveenkumar M",
    'website': "https://catalystsolutions.sg",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_tax_mapping_view.xml',
        'wizard/cm_tax_mapping_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_tax_mapping/static/src/views/*.js',
            'cm_tax_mapping/static/src/**/*.xml',
            'cm_tax_mapping/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
