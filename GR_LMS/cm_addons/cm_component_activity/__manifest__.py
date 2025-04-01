
# -*- coding: utf-8 -*-
{
    'name': "Component / Activity",

    'summary': "This is a custom component / activity",

    'description': """Scope of this module to fulfill the necessary features related to common component / activity form.""",

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
        'views/cm_component_activity_view.xml',
        'wizard/cm_component_activity_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_component_activity/static/src/views/*.js',
            'cm_component_activity/static/src/**/*.xml',
            'cm_component_activity/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
