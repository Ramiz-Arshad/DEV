from odoo import api, models, fields,_
from odoo.exceptions import Warning


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    document_checked = fields.Boolean(string="Document Checked?")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    attachment_ids = fields.One2many('ir.attachment','sale_order_id', string="Product document list")
    document_count = fields.Integer(string="Document Count", compute="compute_document_count")

    def compute_document_count(self):
        for order in self:
            order.document_count = len(order.attachment_ids)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.order_line:
            service_order_line = self.order_line.filtered(lambda l:l.product_id.type == 'service')
            if service_order_line:
                document_uncheck_line = service_order_line.filtered(lambda l: not l.document_checked)
                if document_uncheck_line:
                    raise Warning(_('There are some service product in order line please Generate Documents'))
        if self.attachment_ids:
            document_without_document = self.attachment_ids.filtered(lambda l:l.mandatory and not l.datas)
            if document_without_document:
                lst = [each.document_type for each in document_without_document]
                raise Warning(_('You cannot confirm this order because you do not have attached the %s document'%', '.join([str(elem) for elem in lst])))
        return res

    def action_view_attachment(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        action['domain'] = str([
            ('sale_order_id', '=', self.id)
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action

    def action_create_document(self):
        if self.order_line:
            service_order_line = self.order_line.filtered(lambda l:l.product_id.type == 'service' and not l.document_checked)
            if service_order_line:
                product_lst = []
                for each in service_order_line:
                    if each.product_id.id not in product_lst:
                        product_lst.append(each.product_id.id)
                product_ids = self.env['product.product'].browse(product_lst)
                for product in product_ids:
                    doc_already_generated = False
                    if self.attachment_ids:
                        check_product_doc = self.sudo().attachment_ids.filtered(lambda l:l.product_id.id == product.id)
                        if check_product_doc:
                            doc_already_generated = True
                    if not doc_already_generated:
                        if product.prod_doc_list:
                            for prod_doc in product.prod_doc_list:
                                self.env['ir.attachment'].sudo().create({
                                    'sale_order_id': self.id,
                                    'document_type': prod_doc.document_type,
                                    'mandatory': prod_doc.mandatory,
                                    'product_id': product.id,
                                    'name': prod_doc.document_type
                                })
                service_order_line.write({
                    'document_checked': True
                })


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    document_type = fields.Char(string="Name")
    mandatory = fields.Boolean(string="Mandatory")
    product_id = fields.Many2one('product.product')