from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    published_book_ids = fields.One2many(
        "library.book", "publisher_id", string="Published Books"
    )
    authored_book_ids = fields.Many2many(
        "library.book",
        string="Authored Books",
    )
    count_books = fields.Integer(
        'Number of Authored Books',
        compute='_compute_count_books',
    )

    @api.depends('authored_books_ids')
    def _compute_count_books(self):
        for rec in self:
            rec.count_books = len(rec.authored_books_ids)
