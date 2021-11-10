from odoo import api, models, fields


class ModelloDocumenti(models.Model):
    _name = 'modello.documenti'
    _description = 'modello.documenti'

    name = fields.Char(string="Description", required="1")
    type_document_list = fields.One2many('dett.mod.documenti','modello_id',string="Type document list")


class DettModDocumenti(models.Model):
    _name = 'dett.mod.documenti'
    _description = 'dett.mod.documenti'

    modello_id = fields.Many2one('modello.documenti', string="Model Document")
    type_document = fields.Char(string="Type Document", required=True)
    mandatory = fields.Boolean(string="Mandatory")