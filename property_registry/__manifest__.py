# -*- coding: utf-8 -*-

{
    'name': 'property registry',
    'version': '1.0',
    'summary': """Insertion of property registry
""",
    'author': 'Apulia Software srlu',
    'company': 'Apulia Software srlu',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'view/property_list.xml',
        'view/res_partner.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
