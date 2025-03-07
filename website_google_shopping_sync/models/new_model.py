import base64
import io
import xml.etree.ElementTree as ET
from odoo import models, fields, api

class NewModel(models.Model):
    _name = 'new.model'
    _description = 'New Model for Name and Surname'

    recipient = fields.Char('Recipient', required=True)
    useToken = fields.Boolean('Use Token', required=True)
    accessToken = fields.Char('Access Token', required=True)
    fileName = fields.Char('File Name', required=True)
    use_model = fields.Selection([
        ('product', 'Product'),
        ('product_template', 'Product Template'),
    ], string='Use Model', default='product', required=True)
    file_format = fields.Selection([
        ('csv', 'CSV'),
        ('tsv', 'TSV'),
        ('xml', 'XML'),
    ], string='File Format', default='csv', required=True)
    currency_position = fields.Selection([
        ('by_default', 'By Default'),
        ('before_price', 'Before Price'),
        ('after_price', 'After Price'),
        ('without_currency_code', 'Without Currency Code'),
    ], string="Currency Position", default="by_default")
    stock_mode = fields.Selection([
        ('outOfStock', 'Out Of Stock'),
        ('forecast', 'Forecast Quantity'),
        ('freeToUse', 'Free To Use Quantity'),
    ], string="Out Of Stock mode", default="outOfStock")

    # Add a computed field to show the total product count
    product_count = fields.Integer(
        string='Total Products', compute='_compute_product_count', store=False
    )

    @api.depends('use_model')
    def _compute_product_count(self):
        if self.use_model == 'product':
            self.product_count = self.env['product.product'].search_count([])
        else:
            self.product_count = 0

    def action_download(self):
        # Initialize the data to be used in the file
        if self.use_model == 'product':
            products = self.env['product.product'].search([])

        # Handling file generation based on selected file format
        if self.file_format == 'csv' or self.file_format == 'tsv':
            # Prepare CSV/TSV content
            output = io.StringIO()
            delimiter = ',' if self.file_format == 'csv' else '\t'
            writer = csv.writer(output, delimiter=delimiter)

            # Write header row
            writer.writerow(['Product Name', 'Price', 'Availability'])

            # Write product rows
            for product in products:
                writer.writerow([product.name, product.list_price, product.qty_available])

            # Base64 encode the content
            file_data = base64.b64encode(output.getvalue().encode())

        elif self.file_format == 'xml':
            # Prepare XML content in the desired format
            root = ET.Element("items")
            for product in products:
                item_elem = ET.SubElement(root, "item")

                # g:id
                id_elem = ET.SubElement(item_elem, "g:id")
                id_elem.text = str(product.id)

                # g:title
                title_elem = ET.SubElement(item_elem, "g:title")
                title_elem.text = product.name

                # g:link
                link_elem = ET.SubElement(item_elem, "g:link")
                link_elem.text = f"http://localhost:8069/shop/product/{product.id}"

                # g:image_link
                image_link_elem = ET.SubElement(item_elem, "g:image_link")
                image_link_elem.text = f"http://localhost:8069/web/image/product.product/{product.id}/image/800x800"

                # g:condition
                condition_elem = ET.SubElement(item_elem, "g:condition")
                condition_elem.text = "new"  # Assuming all products are new

                # g:availability
                availability_elem = ET.SubElement(item_elem, "g:availability")
                availability_elem.text = "in stock" if product.qty_available > 0 else "out of stock"

                # g:price
                price_elem = ET.SubElement(item_elem, "g:price")
                price_elem.text = f"{product.list_price} INR"

                # g:shipping
                shipping_elem = ET.SubElement(item_elem, "g:shipping")
                service_elem = ET.SubElement(shipping_elem, "g:service")
                service_elem.text = "Standard"
                shipping_price_elem = ET.SubElement(shipping_elem, "g:price")
                shipping_price_elem.text = "0.0 INR"

                # g:product_type
                product_type_elem = ET.SubElement(item_elem, "g:product_type")
                product_type_elem.text = "Desks"  # Modify as per your product categories

                # g:sale_price
                sale_price_elem = ET.SubElement(item_elem, "g:sale_price")
                sale_price_elem.text = f"{product.list_price * 0.8} INR"  # Example discount (80% of price)

                # g:identifier_exists
                identifier_elem = ET.SubElement(item_elem, "g:identifier_exists")
                identifier_elem.text = "false"

            # Convert XML tree to string
            tree = ET.ElementTree(root)
            xml_data = io.BytesIO()
            tree.write(xml_data, encoding='utf-8', xml_declaration=True)

            # Base64 encode the XML file
            xml_data.seek(0)
            file_data = base64.b64encode(xml_data.read())

        # Create attachment in Odoo
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.fileName}.{self.file_format}',
            'type': 'binary',
            'datas': file_data,
            'mimetype': 'application/octet-stream',  # Generic mime type for downloadable files
            'res_model': 'new.model',
            'res_id': self.id,
        })

        # Return an action to download the attachment
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'new',
        }
