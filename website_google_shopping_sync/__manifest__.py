###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2020-Today Trey, Kilobytes de Soluciones <www.trey.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Google Shopping Sync',
    'category': 'e-commerce',
    'summary': 'Generate products feed for Google Merchant Center',
    'version': '18.0.1.0.0',
    'author': 'Trey (www.trey.es)',
    'website': 'https://cnelindia.com/',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'stock',
        'website_sale',
    ],
    # 'post_init_hook': 'post_init_hook',
    'data': [
        'security/ir.model.access.csv',
        'templates/website_sale_template.xml',
        'views/product_views.xml',
        'views/product_pricelist_views.xml',
        'views/res_company_views.xml',
        'views/website_views.xml',
        'views/google_product_category_views.xml',
        'views/new_model_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'website_google_shopping_sync/static/src/css/style.css',  # Add the CSS file here
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    # 'post_init_hook': 'post_init_hook',
    'sequence': 4,
}

