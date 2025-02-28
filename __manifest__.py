{
    'name': 'Fee Collections',
    'version': '1.0.0',
    'summary': 'Fee Collections',
    'description': """
        A more detailed description of the module.
    """,
    'author': 'Murshid',
    'website': 'https://www.yourwebsite.com',
    'category': 'Specific Category',
    'license': 'LGPL-3',
    'depends': [
        'base','website', 'openeducat_core'  # List of module dependencies

        # Add other module dependencies here
    ],
    'data': [
        # 'security/ir.model.access.csv',  # Access rights
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/quick_pay_report.xml',
        # 'views/payment.xml',
        'views/payment_web_form.xml'

    ],

    'installable': True,
    'application': False,
    'auto_install': False,

}
