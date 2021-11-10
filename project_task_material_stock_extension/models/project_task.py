# Copyright 2021 Apulia Software - Nicola Malcontenti
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import _, api, exceptions, fields, models


class Task(models.Model):
    _inherit = "project.task"

    material_ids = fields.One2many(
        comodel_name="project.task.material",
        inverse_name="task_id",
        string="Material Used",
        copy=True
    )

    @api.onchange("project_id")
    def on_change_is_template(self):
        if self.project_id.analytic_account_id:
            self.analytic_account_id = self.project_id.analytic_account_id

    def action_view_pickings(self):
        self.ensure_one()
        list_of_picking = []
        for move in self.stock_move_ids:
            if move.picking_id.id in list_of_picking:
                continue
            else:
                list_of_picking.append(move.picking_id.id)
        tree_id = self.env.ref('stock.vpicktree').id
        form_id = self.env.ref('stock.view_picking_form').id
        return {
            'name': 'Picking',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(tree_id,'tree'),(form_id, 'form')],
            'res_model': 'stock.picking',
            'domain': [('id', 'in', list_of_picking)]
        }

    
class ProjectProject(models.Model):
    
    _inherit = 'project.project'
    
    delivery_address_id = fields.Many2one('res.partner')
    

class ProjectTaskMaterial(models.Model):
    
    _inherit = "project.task.material"
    
    def create_stock_move(self):
        pick_type = self.env.ref(
            "project_task_material_stock.project_task_material_picking_type"
        )
        task = self[0].task_id
        delivery_addr = task.partner_id.id
        if task.project_id.delivery_address_id:
            delivery_addr = task.project_id.delivery_address_id
        picking_id = task.picking_id or self.env["stock.picking"].create(
            {
                "origin": "{}/{}".format(task.project_id.name, task.name),
                "partner_id": delivery_addr.id,
                "picking_type_id": pick_type.id,
                "location_id": pick_type.default_location_src_id.id,
                "location_dest_id": pick_type.default_location_dest_id.id,
            }
        )
        for line in self:
            if not line.stock_move_id:
                move_vals = line._prepare_stock_move()
                move_vals.update({"picking_id": picking_id.id or False})
                move_id = self.env["stock.move"].create(move_vals)
                line.stock_move_id = move_id.id
    