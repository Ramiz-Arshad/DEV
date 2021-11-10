from odoo import api, models, fields,_
from odoo.exceptions import Warning

class AccountMove(models.Model):
    _inherit = 'account.move'

    credit_custom_move_id = fields.Many2one('account.move')
    tax_deduction = fields.Many2one('tax.credit.discount', string="Tax Deduction", compute="get_discount_data")
    invoice_discount = fields.Monetary(string="Invoice Discount", compute="get_discount_data")
    amount_discounted = fields.Monetary(string="Total Amount Discounted", compute="get_discount_data")

    def get_discount_data(self):
        for each in self:
            each.tax_deduction = False
            each.invoice_discount = 0
            each.amount_discounted = 0
            if each.invoice_line_ids and each.invoice_line_ids[0].sale_line_ids:
                order_id = each.invoice_line_ids[0].sale_line_ids[0].order_id
                each.tax_deduction = order_id.tax_deduction
                each.invoice_discount = order_id.invoice_discount
                each.amount_discounted = order_id.amount_discounted

    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        move_ids = self.env['account.move'].sudo().search([('credit_custom_move_id', '=', self.id)])
        if move_ids:
            for each in move_ids:
                each.button_draft()
                each.button_cancel()
                each.with_context(force_delete=True).unlink()
        return res

    def action_post(self):
        res = super(AccountMove, self).action_post()
        order_id = False
        if self.invoice_line_ids[0].sale_line_ids:
            order_id = self.invoice_line_ids[0].sale_line_ids[0].order_id
        if order_id:
            move_ids = self.env['account.move'].sudo().search([('credit_custom_move_id', '=', self.id)])
            if not move_ids:
                if (self.tax_deduction and self.tax_deduction.discount_percentage and not self.tax_deduction.extra_debit_account_id and not self.tax_deduction.extra_credit_account_id):
                    move_id = self.env['account.move'].sudo().create({
                        'move_type': 'entry',
                        'ref': order_id.name + " " + "Generic case: Deduction " + " " + self.tax_deduction.name,
                        'partner_id': self.partner_id.id,
                        'journal_id': self.tax_deduction.journal_id.id,
                        'currency_id': self.currency_id.id,
                        'credit_custom_move_id': self.id,
                        'line_ids': [(0, 0, {
                            'account_id': self.tax_deduction.credit_account_id.id,
                            'partner_id': self.partner_id.id,
                            'credit': self.invoice_discount,
                            'currency_id': self.currency_id.id,
                        }),
                                     (0, 0, {
                                         'account_id': self.tax_deduction.debit_account_id.id,
                                         'partner_id': self.partner_id.id,
                                         'debit': self.invoice_discount,
                                         'currency_id': self.currency_id.id,
                                     })
                                     ]
                    })
                    if move_id and move_id.state == 'draft':
                        move_id.action_post()
                        print ("\n\n\ posr===============")
                if (self.tax_deduction.extra_credit_account_id and self.tax_deduction.extra_debit_account_id and self.tax_deduction.extra_discount_percentage):
                    move_id = self.env['account.move'].sudo().create({
                        'move_type': 'entry',
                        'ref': order_id.name + " " + "Exceptional of case " + " " + self.tax_deduction.name,
                        'partner_id': self.partner_id.id,
                        'journal_id': self.tax_deduction.journal_id.id,
                        'currency_id': self.currency_id.id,
                        'credit_custom_move_id': self.id,
                        'line_ids': [
                            (0, 0, {
                                'account_id': self.tax_deduction.credit_account_id.id,
                                'partner_id': self.partner_id.id,
                                'credit': self.invoice_discount,
                                'currency_id': self.currency_id.id,
                            }),
                            (0, 0, {
                                'account_id': self.tax_deduction.debit_account_id.id,
                                'partner_id': self.partner_id.id,
                                'debit':self.invoice_discount,
                                'currency_id': self.currency_id.id,
                            }),
                            (0, 0, {
                                'account_id': self.tax_deduction.extra_credit_account_id.id,
                                'partner_id': self.partner_id.id,
                                'credit': self.amount_total * self.tax_deduction.extra_discount_percentage / 100,
                                'currency_id': self.currency_id.id,
                            }),
                            (0, 0, {
                                'account_id': self.tax_deduction.extra_debit_account_id.id,
                                'partner_id': self.partner_id.id,
                                'debit': self.amount_total * self.tax_deduction.extra_discount_percentage  / 100,
                                'currency_id': self.currency_id.id,
                            }),
                        ]
                    })
                    if move_id and move_id.state == 'draft':
                        move_id.action_post()
        return res



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tax_deduction = fields.Many2one('tax.credit.discount', string="Tax Deduction")
    invoice_discount = fields.Monetary(string="Invoice Discount", compute="compute_tax_credit_discount")
    amount_discounted = fields.Monetary(string="Total Amount Discounted", compute="compute_amount_discounted")

    @api.depends('tax_deduction','amount_total')
    def compute_amount_discounted(self):
        for each in self:
            each.amount_discounted = 0
            if each.tax_deduction:
                each.amount_discounted = each.amount_total - each.invoice_discount

    @api.depends('tax_deduction','amount_total')
    def compute_tax_credit_discount(self):
        for each in self:
            each.invoice_discount = 0
            if each.tax_deduction:
                each.invoice_discount = each.amount_total * each.tax_deduction.discount_percentage / 100


class TaxCreditDiscount(models.Model):
    _name = 'tax.credit.discount'

    name = fields.Char(string="Description", required=True)
    discount_percentage = fields.Float(string="Percentage")
    journal_id = fields.Many2one('account.journal', string="Journal")
    debit_account_id = fields.Many2one('account.account', string="Debit Account")
    credit_account_id = fields.Many2one('account.account', string="Credit Account")
    extra_debit_account_id = fields.Many2one('account.account', string="Extra Debit Account")
    extra_credit_account_id = fields.Many2one('account.account', string="Extra Credit Account")
    extra_discount_percentage = fields.Float(string="Extra Discount Percentage")
