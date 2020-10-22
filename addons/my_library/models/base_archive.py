from odoo import api, fields, models


class BaseArchive(models.AbstractModel):
    _name = "base.archive"

    active = fields.Boolean(default=True)

    def do_archive(self):
        for rec in self:
            rec.active = not rec.active
