###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    google_title = fields.Char(
        string='Google Title',
        compute='_compute_google_title',
    )

    @api.depends('name', 'product_tmpl_id.attribute_value_ids')
    def _compute_google_title(self):
        for product in self:
            google_title = product.name
            var_title = [
                '%s %s' % (a.attribute_id.name, a.name) for a in
                product.product_tmpl_id.attribute_value_ids]
            product.google_title = '%s%s' % (
                google_title,
                var_title and ' - %s' % ' '.join(var_title) or '',
            )

