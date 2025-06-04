from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class SalesOrderExtension(models.Model):
    _inherit = "sale.order"

    total_products_qty = fields.Float(compute="_compute_total_products_qty", string="Total Products Quantity", store=True)
    is_high_value = fields.Boolean(compute="_compute_is_high_value", store=True, default=False, read_only=True, string="Is High Value")


    def print_custom_pdf(self):
        return self.env.ref('sales_extension.sale_extension_report').report_action(self)


    @api.depends("order_line.product_uom_qty")
    def _compute_total_products_qty(self):
        for rec in self:
            rec.total_products_qty = sum(line.product_uom_qty for line in rec.order_line)

    @api.depends("amount_total")
    def _compute_is_high_value(self):
        for rec in self:
            if rec.amount_total > 50000:
                rec.is_high_value = True
            else:
                rec.is_high_value = False