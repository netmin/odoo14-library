from odoo import fields, models


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"
    _order = "date_release desc, name"
    _rec_name = "short_name"

    name = fields.Char("Title", required=True)
    short_name = fields.Char(
        "Short Title",
        required=True,
        translate=True,
        index=True,
    )
    notes = fields.Text("Internal Notes")
    state = fields.Selection(
        [
            ("draft", "Not Available"),
            ("available", "Available"),
            ("lost", "Lost"),
        ],
        "State",
        default="draft",
    )
    description = fields.Html("Description", sanitize=True, strip_style=False)
    cover = fields.Binary("Book Cover")
    out_of_print = fields.Boolean("Out of Print?")
    date_release = fields.Date("Release Date")
    date_updated = fields.Datetime("Last Updated")
    pages = fields.Integer(
        "Number of Pages",
        groups="base.group_user",
        states={"lost": [("readonly", True)]},
        help="Total book page count",
        company_dependent=False,
    )
    reader_rating = fields.Float("Reader Average Rating", digits=(14, 4))
    author_ids = fields.Many2many("res.partner", string="Authors")
    currency_id = fields.Many2one(
        "res_currency",
        string="Currency",
    )
    cost_price = fields.Monetary("Cost Price")
    retail_price = fields.Monetary("Retail Price")
    publisher_id = fields.Many2one(
        "res.partner",
        string="Publisher",
    )
    category_id = fields.Many2one("library.book.category")
