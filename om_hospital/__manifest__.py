# -- coding: utf-8 --
{
    'name': "Hospital Management",
    'sequence': '-100',
    'summary': """
    Hospital management system
        """,

    'description': """
    Hospital management system
    """,

    'author': "shehab nasser",
    'website': "http://www.yourcompany.com",

    'category': 'Hospital',
    'version': '1.0.0',

    'depends': ['mail', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/patient_sequence.xml',
        'data/appointment_sequence.xml',
        'wizard/cancel_appointment_view.xml',
        'views/odoo_playground.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
    ],
    # 'data': [
    #     # 'data/data.xml',
    # ],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
