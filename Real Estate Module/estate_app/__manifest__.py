{
    'name': "Estate App",
    'version': "1.2",
    'depends': ["base","website"],
    'author': "YAGP@ODOO.COM",
    'category': "Real Estate/Estate",
    'summary': "The One and Only Best Real Estate App Availble on Odoo!",
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "security/ir.rule.xml",
        "views/offer_views.xml",
        "views/type_views.xml",
        "views/tag_views.xml",
        "views/menus_action.xml",
        "views/property_views.xml",
        "views/estate_menus.xml",
        "data/demo_data.xml",
        "views/estate_res_users_views.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "views/templates.xml",
        "wizard/estate_property_offer_wizard_view.xml",
    ],
    'license': "LGPL-3",
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
        Odoo Estate App
        ===============
        The Only App You Need To Manage Your All Properties. Buy,Sell,Rent Everything is Here!!
        """
}
