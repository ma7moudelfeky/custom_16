# Copyright 2016 Cédric Pigeon, ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Add More Product",
    "summary": """
        Sale Add More Product """,
    "category": "Sale Management",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale", 'sale_customize'],
    "data": [
        "security/ir.model.access.csv",
        "wizards/sale_import_products_view.xml",
        "views/sale_view.xml",
    ],
}
