{
    'name': "Estate Account",
    'version': "1.0",
    'depends': ["account","estate_app"],
    'author': "YAGP@ODOO.COM",
    'category': "Real Estate",
    'summary': "Accounting Module For Your Real Estate App.",
    'data': [
        "security/ir.model.access.csv",
        "report/inherit_estate_property_templates.xml"
    ],
    'license': "LGPL-3",
    'module_type': 'official',
    'installable': True,
    'application': True,
    'auto_install': True,
    'description': """
        Odoo Estate Account
        ===============
        Manage Your Invoices Here!
        """
}
