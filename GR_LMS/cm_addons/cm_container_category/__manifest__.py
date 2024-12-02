# -*- coding: utf-8 -*-
{
    'name': "Container Category",

    'summary': "This is a custom container category",

    'description': """Scope of this module to fulfill the necessary features related to container category form.""",

    'author': "Bharath",
    'website': "https://www.goodrich.co",
    'category': 'Catalyst/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_container_category_view.xml',
        'wizard/cm_container_category_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_container_category/static/src/views/*.js',
            'cm_container_category/static/src/**/*.xml',
            'cm_container_category/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}

