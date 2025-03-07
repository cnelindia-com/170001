from odoo import http
from odoo.http import request

class GoogleShoppingSync(http.Controller):

    @http.route('/google-shopping-sync.xml', auth='public', type='http', website=True)
    def google_shopping_sync(self, **kwargs):
        products = request.env['product.product'].search([])  # All products fetch
        items = []

        for product in products:
            # Construct the URL to the product page on your shop
            product_url = f'http://localhost:8069/shop/product/{product.id}'
            image_url = f'http://localhost:8069/web/image/product.product/{product.id}/image/800x800?unique={product.id}'
            
            # Example sale price calculation (you can modify this logic as per your needs)
            sale_price = product.lst_price * 0.9  # Assuming a 10% discount
            
            product_data = {
                'g:id': product.id,
                'g:title': product.name,
                'g:link': product_url,
                'g:image_link': image_url,
                'g:condition': 'new',
                'g:availability': 'in stock' if product.qty_available > 0 else 'out of stock',
                'g:price': f'{product.list_price} INR',
                'g:shipping': {
                    'g:service': 'Standard',
                    'g:price': '0.0 INR',
                },
                'g:product_type': product.categ_id.name if product.categ_id else '',
                'g:sale_price': f'{sale_price} INR',
                'g:identifier_exists': 'false',  # Assuming products don't have identifiers
            }
            items.append(product_data)

        # Constructing XML feed
        feed = """
        <rss version="2.0">
            <channel>
                <title>YourCompany</title>
                <link>http://localhost:8069</link>
        """
        
        for item in items:
            feed += f"""
            <item>
                <g:id>{item['g:id']}</g:id>
                <g:title>{item['g:title']}</g:title>
                <g:link>{item['g:link']}</g:link>
                <g:image_link>{item['g:image_link']}</g:image_link>
                <g:condition>{item['g:condition']}</g:condition>
                <g:availability>{item['g:availability']}</g:availability>
                <g:price>{item['g:price']}</g:price>
                <g:shipping>
                    <g:service>{item['g:shipping']['g:service']}</g:service>
                    <g:price>{item['g:shipping']['g:price']}</g:price>
                </g:shipping>
                <g:product_type>{item['g:product_type']}</g:product_type>
                <g:sale_price>{item['g:sale_price']}</g:sale_price>
                <g:identifier_exists>{item['g:identifier_exists']}</g:identifier_exists>
            </item>
            """
        
        feed += """
            </channel>
        </rss>
        """

        return feed
