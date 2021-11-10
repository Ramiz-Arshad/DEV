# -*- coding: utf-8 -*-

{
    'name': 'Document Collection',
    'version': '1.0',
    'summary': """Collection of documents by project
""",
    'author': 'Apulia Software srlu',
    'company': 'Apulia Software srlu',
    'depends': ['base', 'sale','project', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'view/document.xml',
        'view/product.xml',
        'view/sale.xml',
        'view/project_task.xml',
        'wizard/task_document.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
