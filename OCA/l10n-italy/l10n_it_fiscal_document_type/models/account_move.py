from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("partner_id", "journal_id", "move_type", "fiscal_position_id")
    def _compute_set_document_fiscal_type(self):
        for invoice in self:
            if invoice.state != "draft" and invoice.fiscal_document_type_id:
                continue
            invoice.fiscal_document_type_id = False
            dt = invoice._get_document_fiscal_type(
                invoice.move_type,
                invoice.partner_id,
                invoice.fiscal_position_id,
                invoice.journal_id,
            )
            if dt:
                invoice.fiscal_document_type_id = dt[0]

    def _get_document_fiscal_type(
        self, move_type=None, partner=None, fiscal_position=None, journal=None
    ):
        dt = []
        doc_id = False
        if not move_type:
            move_type = "out_invoice"

        # Partner
        if partner:
            if move_type in ("out_invoice"):
                doc_id = partner.out_fiscal_document_type.id or False
            elif move_type in ("in_invoice"):
                doc_id = partner.in_fiscal_document_type.id or False
        # Fiscal Position
        if not doc_id and fiscal_position:
            doc_id = fiscal_position.fiscal_document_type_id.id or False
        # Journal
        if not doc_id and journal:
            dt = (
                self.env["fiscal.document.type"]
                .search([("journal_ids", "in", [journal.id])])
                .ids
            )
        if (
            not doc_id
            and not dt
            and move_type in ["out_invoice", "out_refund", "in_invoice", "in_refund"]
        ):
            dt = self.env["fiscal.document.type"].search([(move_type, "=", True)]).ids

        # Refund Document type
        if (dt or doc_id) and "refund" in move_type:
            fdt = self.env["fiscal.document.type"].browse(doc_id or dt[0])
            if (
                fdt
                and not fdt.out_refund
                and not fdt.in_refund
                and fdt.refund_fiscal_document_type_id
            ):
                if dt:
                    dt[0] = fdt.refund_fiscal_document_type_id.id
                else:
                    dt.append(fdt.refund_fiscal_document_type_id.id)

        if doc_id:
            dt.append(doc_id)
        return dt

    fiscal_document_type_id = fields.Many2one(
        "fiscal.document.type",
        string="Fiscal Document Type",
        compute="_compute_set_document_fiscal_type",
        store=True,
        readonly=False,
    )

    def _reverse_move_vals(self, default_values, cancel=True):
        vals = super()._reverse_move_vals(default_values, cancel)
        # when reversing a move, fiscal_document_type_id should be recomputed, not copied
        if "fiscal_document_type_id" in vals:
            del vals["fiscal_document_type_id"]
        return vals
