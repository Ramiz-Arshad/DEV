from odoo import api, models, fields,_
from odoo.exceptions import Warning


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def attachment_tree_view(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        if self.sale_order_id:
            action['domain'] = str([
                '|',
                '|',
                '&',
                ('res_model', '=', 'project.project'),
                ('res_id', 'in', self.ids),
                '&',
                ('res_model', '=', 'project.task'),
                ('res_id', 'in', self.task_ids.ids),
                ('sale_order_id','=',self.sale_order_id.id)
            ])
        else:
            action['domain'] = str([
                '|',
                '&',
                ('res_model', '=', 'project.project'),
                ('res_id', 'in', self.ids),
                '&',
                ('res_model', '=', 'project.task'),
                ('res_id', 'in', self.task_ids.ids)
            ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action

    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for project in self:
            if self.sale_order_id:
                project.doc_count = Attachment.search_count([
                    '|',
                    '|',
                    '&',
                    ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                    '&',
                    ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids),
                    ('sale_order_id','=',self.sale_order_id.id)
                ])
            else:
                project.doc_count = Attachment.search_count([
                    '|',
                    '&',
                    ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                    '&',
                    ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)
                ])

class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_doc_list = fields.One2many('ir.attachment','task_id')
    all_document_collected = fields.Integer(string="Document Collected?", compute="check_document")

    def check_document(self):
        for each in self:
            each.all_document_collected = 0
            att_ids = each.task_doc_list
            if each.task_doc_list:
                att_ids = each.task_doc_list.filtered(lambda l:l.mandatory)
            if att_ids:
                att_line_ids = att_ids.filtered(lambda l:l.datas == False)
                if not att_line_ids:
                    each.all_document_collected = 1
            else:
                if each.task_doc_list:
                    att_line_ids = att_ids.filtered(lambda l: l.datas == False)
                    if not att_line_ids:
                        each.all_document_collected = 1

    def create_document(self):
        return {'view_mode': 'form',
                'res_model': 'task.document',
                'view_type': 'form',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context' : {'rec_id': self.id}
                }

    def export_zip(self):
        tab_id = []
        for each in self.task_doc_list:
            if each.datas:
                tab_id.append(each.id)
        url = '/web/binary/download_document?tab_id=%s' % tab_id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def export_zip_send_email(self):
        pass

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    task_id = fields.Many2one('project.task', string="Task")
    origin_list = fields.Many2one('modello.documenti', string="Origin list")
    dett_mod_line_id = fields.Many2one('dett.mod.documenti')