
# -*- coding: utf-8 -*-
{
    'name': "Depot Job Sequence",

    'summary': "This is a custom depot job sequence",

    'description': """Scope of this module to fulfill the necessary features related to common depot job sequence form.""",

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
        'views/cm_depot_job_sequence_view.xml',
        'wizard/cm_depot_job_sequence_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_depot_job_sequence/static/src/views/*.js',
            'cm_depot_job_sequence/static/src/**/*.xml',
            'cm_depot_job_sequence/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
