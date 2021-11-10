from odoo import api, models, fields,_
from odoo.exceptions import Warning

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def fetch_document_list(self):
        document_lst = []
        for each in self.model_document_id.type_document_list:
            document_lst.append((0,0,{
                'document_type': each.type_document,
                'mandatory' : each.mandatory
            }))
        self.prod_doc_list.unlink()
        self.prod_doc_list = document_lst


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    model_document_id = fields.Many2one('modello.documenti',string="Model Document")
    prod_doc_list = fields.One2many('product.document.list','product_id',string="Product Document List")

    def fetch_document_list(self):
        document_lst = []
        for each in self.model_document_id.type_document_list:
            document_lst.append((0,0,{
                'document_type': each.type_document,
                'mandatory' : each.mandatory
            }))
        self.prod_doc_list.unlink()
        self.prod_doc_list = document_lst

class ProductDocumentList(models.Model):
    _name = 'product.document.list'
    _description = 'Product Document List'

    document_type = fields.Char(string="Document Type")
    product_id = fields.Many2one('product.template', string="Product")
    mandatory = fields.Boolean(string="Mandatory")