# ###############################################################################
# # For copyright and license notices, see __manifest__.py file in root directory
# ###############################################################################
# import odoo
# import logging
# from odoo import SUPERUSER_ID, api
# import os

# _logger = logging.getLogger(__name__)

# def post_init_hook(cr, registry):
#     """
#     Import Google Product Taxonomies:
#     https://support.google.com/merchants/answer/1705911?hl=en
#     """
#     with api.Environment.manage():
#         env = api.Environment(cr, SUPERUSER_ID, {})
#         lang = env.context.get('lang', 'en_US')
        
#         # Google Product Category Model
#         category = env['google_product_category']
        
#         # Get module path
#         path = odoo.modules.module.get_module_path('website_sale_google_shopping')
#         _logger.info("Looking for file at path: %s", path + '/data/taxonomy-with-ids.%s.txt' % lang.replace('_', '-'))

#         # Build full file path
#         file_path = path + '/data/taxonomy-with-ids.%s.txt' % lang.replace('_', '-')
        
#         # Check if the file exists
#         if os.path.exists(file_path):
#             _logger.info("File found: %s", file_path)
#             with open(file_path, 'r') as taxonomies_file:
#                 for line in taxonomies_file:
#                     data = line.split(' - ')
#                     if len(data) > 1:
#                         category.create({
#                             'google_id': data[0],
#                             'name': data[1],
#                         })
#         else:
#             _logger.error("File not found: %s", file_path)


