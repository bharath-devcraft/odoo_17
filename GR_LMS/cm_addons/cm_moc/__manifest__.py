
# -*- coding: utf-8 -*-
{
    'name': "Moc",

    'summary': "This is a custom moc",

    'description': """Scope of this module to fulfill the necessary features related to common moc form.""",

    'author': "Praveenkumar M",
    'website': "https://www.goodrich.co",
    'category': 'Custom Modules/custom_modules',
    'application' : True,
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/audit_rule_data.xml',
        'data/security_rule.xml',
        'views/cm_moc_view.xml',
        'wizard/cm_moc_batch_inactive_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cm_moc/static/src/views/*.js',
            'cm_moc/static/src/**/*.xml',
            'cm_moc/static/src/**/*.css',
        ],
    },
    
    'license': 'LGPL-3',
}
