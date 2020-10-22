from odoo import fields, models, api
from datetime import timedelta


class LibraryBook(models.Model):
    _name = "library.book"
    _inherit = ["base.archive"]
    _description = "Library Book"
    _order = "date_release desc, name"
    _rec_name = "short_name"
    _sql_constraints = [("name_uniq", "UNIQUE (name)", "Book title must be unique")]

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
    publisher_city = fields.Char(
        "Publisher City",
        related="publisher_id.city",
        readonly=True,
    )
    category_id = fields.Many2one("library.book.category")
    age_days = fields.Float(
        string="Days Since Release",
        compute="_compute_age",
        inverse="_inverse_age",
        search="_search_age",
    )
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document'
    )

    @api.constrains("date_release")
    def _check_release_date(self):
        for rec in self:
            if rec.date_release > fields.Date.today():
                raise models.ValidationError("Release date must be in the past")

    @api.depends("date_release")
    def _compute_age(self):
        today = fields.Date.today()
        for book in self.filtered("date_release"):
            delta = today - book.date_release
            book.age_days = delta.days

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered("date_release"):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        operator_map = {
            ">": "<",
            ">=": "<=",
            "<": ">",
            "<=": ">=",
        }
        new_op = operator_map.get(operator, operator)
        return [("date_release", new_op, value_date)]

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([
            ('field_id.name', '=', 'message_ids')
        ])
        return [(x.model, x.name) for x in models]
