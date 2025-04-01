
# -*- coding: utf-8 -*-
{
    'name': "Nature Of Job",

    'summary': "This is a custom nature of job",

    'description': """Scope of this module to fulfill the necessary features related to common nature of job form.""",

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
        'views/cm_nature_of_job_view.xml',
        'wizard/cm_nature_of_job_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_nature_of_job/static/src/views/*.js',
            'cm_nature_of_job/static/src/**/*.xml',
            'cm_nature_of_job/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
