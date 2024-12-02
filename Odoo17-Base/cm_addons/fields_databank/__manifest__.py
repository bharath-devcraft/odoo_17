# -*- coding: utf-8 -*-
{
    'name': "Fields Databank",
    'version': '0.1',
    'summary': "Fields collection for Development",
    'description': """
            Collection of the fields with the business logic and validation.
    """,
    'author': "Hari",
    'category': "KGiSL/custom_modules",
    'application' : True,
    'depends': ['base','product','uom', 'account','cm_master'],
    'data': [
        'security/ir.model.access.csv',
        'views/cm_fields_view.xml',
        'views/ct_key_features_view.xml',
        'views/cm_key_features_view.xml'
    ],
    'assets': {
        'web.assets_backend': {
        },
    },
    'installable': True,
    'license': 'LGPL-3',
}

