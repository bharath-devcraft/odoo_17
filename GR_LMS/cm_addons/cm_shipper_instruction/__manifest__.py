
# -*- coding: utf-8 -*-
{
    'name': "Shipper Instruction",

    'summary': "This is a custom shipper instruction",

    'description': """Scope of this module to fulfill the necessary features related to common shipper instruction form.""",

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
        'views/cm_shipper_instruction_view.xml',
        'wizard/cm_shipper_instruction_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_shipper_instruction/static/src/views/*.js',
            'cm_shipper_instruction/static/src/**/*.xml',
            'cm_shipper_instruction/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
