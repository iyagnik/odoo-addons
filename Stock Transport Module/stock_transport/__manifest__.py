{
    'name': "Transport Management System",
    'version': "1.0",
    'depends': ["stock_picking_batch","fleet"],
    'author': "Yagnik (yagp)",
    'summary': "Transport Management System",
    'category': 'Inventory',
    'data': [
        "security/ir.model.access.csv",
        "views/stock_fleet_views.xml",
        "views/stock_picking_batch_views.xml",
    ],
    'license': "LGPL-3",
    'installable': True,
    'auto_install': False,
    'description': """
        Transport Management System
        ===============
        The 'Transport Management System' module will implement TMS based on picking batches. """,
}
