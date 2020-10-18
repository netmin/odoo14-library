from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    published_book_ids = fields.One2many(
        "library.book", "publisher_id", string="Published Books"
    )
    authored_book_ids = fields.Many2many(
        "library.book",
        string="Authored Books",
    )
