from odoo import api, models, fields


class TaskDocument(models.TransientModel):
    _name = 'task.document'
    _description = 'Task Document'

    document_model_ids = fields.Many2many('modello.documenti', string="Liste Documenti")

    def generate_document(self):
        task_id = self.env['project.task'].sudo().browse(self._context.get('rec_id'))
        for doc in self.document_model_ids:
            for doc_list in doc.type_document_list:
                line = task_id.task_doc_list.filtered(lambda l:l.task_id == task_id and l.dett_mod_line_id == doc_list)
                if not line:
                    self.env['ir.attachment'].sudo().create({
                        'sale_order_id': self.id,
                        'document_type': doc_list.type_document,
                        'mandatory': doc_list.mandatory,
                        'task_id' : task_id.id,
                        'dett_mod_line_id' : doc_list.id,
                        'name': doc_list.type_document
                    })

