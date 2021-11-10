# -*- coding: utf-8 -*-

{
    'name': 'Tax Credit Discount',
    'version': '1.0',
    'summary': """This module create journal entry based on discount model.
""",
    'author': 'Apulia Software srlu',
    'company': 'Apulia Software srlu',
    'depends': ['base', 'account','sale'],
    'data': [
        'security/ir.model.access.csv',
        'view/tax_credit_discount.xml',
        'view/sale.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
