# -*- coding: utf-8 -*-
{
    'name': "TechScope Lisec Integration",

    'summary': """
        TechScope Lisec Integration""",

    'description': """
       TechScope Lisec Integration"
    """,

    'author': "Abdulrahman Rabie, TechScope Team",
    'website': "https://techscopeco.com/",

    'category': 'eCommerce',

    'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/Lisec_Integration_views.xml',
        'views/product.xml',
        'views/sale_order.xml',
    ],
    'demo': [

    ],
}
