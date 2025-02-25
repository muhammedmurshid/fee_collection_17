from odoo import models, fields, api, _
from datetime import date, datetime, time


class FeeQuickPayLogic(models.Model):
    _name = 'fee.quick.pay'
    _description = 'Fee Quick Pay'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    admission_no = fields.Char(string='Admission No')
    # other_client = fields.Char(string='Other Client')
    other_amount = fields.Char(string='Other Amount')
    purpose = fields.Selection(
        [('admission_fee', 'Admission Fee'), ('coaching_fee', 'Coaching Fee'), ('ima_membership', 'IMA Membership'),
         ('ima_exam_payment', 'IMA Exam Payment'), ('acca_board_registration', 'Acca Board Registration'),
         ('acca_exam_payment', 'ACCA Exam Payment'), ('cia_membership_fee', 'CIA Membership Fee'),  ('missing_added', 'Missing Added'),], string='Purpose')
    other_phone = fields.Char(string='Other Phone')
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        default=lambda self: self.env.company.currency_id.id  # Default to the company currency
    )
    role = fields.Char(string='Role')
    email = fields.Char(string="Email", widget="mail")
    # purpose = fields.Char(string='Purpose')
    branch = fields.Char(string='Branch')
    batch = fields.Char(string='Batch')
    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    amount = fields.Float(string='Amount')
    refno = fields.Char(string='Ref No')
    state = fields.Selection([('draft', 'Pending'), ('done', 'Added Wallet')], default="draft")
    reconciliation = fields.Boolean(string="Reconciliation")
    reconciliation_date = fields.Date(string="Reconciliation Date")
    added_date = fields.Datetime(string="Added Date", default=lambda self: datetime.now(),)

    def act_assign_to_wallet(self):
        print('hi')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Students'),
            'res_model': 'op.student',
            'domain': [('mobile', 'ilike', self.phone)],
            'context': {
                # 'active_test': self.active,
                'default_amount': self.amount,
            },
            'view_type': 'tree,form',
            'view_mode': 'tree,form',
        }

    @api.onchange('reconciliation')
    def _onchange_reconciliation(self):
        if self.reconciliation == True:
            self.reconciliation_date = datetime.now()
        else:
            self.reconciliation_date = False
