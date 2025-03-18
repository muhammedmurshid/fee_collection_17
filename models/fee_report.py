from odoo import models, fields, api, _
from datetime import date, datetime, time
from num2words import num2words

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
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
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
    student_id = fields.Many2one('op.student', string="Student")
    assigned_by = fields.Many2one('res.users', string="Assigned By")
    assigned_date = fields.Datetime(string="Assigned Date")
    receipt_no = fields.Char(string="Receipt No",  readonly=True, copy=False)

    @api.depends('amount','purpose')
    def _compute_tax_amount(self):
        for i in self:
            if i.amount != 0:
                if i.purpose in ['admission_fee','coaching_fee','missing_added']:
                    i.tax_amount = i.amount * 18/118
                    print('mur')
                else:
                    print('pur')
                    i.tax_amount = 0

    tax_amount = fields.Float(string="Tax", compute="_compute_tax_amount", store=1)

    @api.depends('tax_amount')
    def _compute_spliting_gst(self):
        for i in self:
            if i.tax_amount != 0:
                i.cgst_amount = i.tax_amount / 2
                i.sgst_amount = i.tax_amount / 2
                i.amount_exc_tax = i.amount - i.tax_amount
            else:
                i.cgst_amount = 0
                i.sgst_amount = 0
                i.amount_exc_tax = i.amount

    cgst_amount = fields.Float(string="CGST", compute="_compute_spliting_gst", store=1)
    sgst_amount = fields.Float(string="SGST", compute="_compute_spliting_gst", store=1)
    amount_exc_tax = fields.Float(string="Exc Tax", compute="_compute_spliting_gst", store=1)
    # @api.model
    # def create(self, vals):
    #     if not vals.get('receipt_no'):
    #         vals['receipt_no'] = self._generate_receipt_number()
    #     return super(FeeQuickPayLogic, self).create(vals)

    def _generate_receipt_number(self):
        """Generate a receipt number based on the financial year (April - March)."""
        today = date.today()
        year = today.year
        if today.month < 4:  # If Jan, Feb, or March, use the previous year
            start_year = year - 1
            end_year = year
        else:
            start_year = year
            end_year = year + 1

        # Format financial year
        fy_string = f"{start_year}-{str(end_year)[-2:]}"

        # Get the last record of the same financial year
        last_receipt = self.search([('receipt_no', 'like', f'RCPT-{fy_string}/%')], order='id desc', limit=1)

        if last_receipt and last_receipt.receipt_no:
            last_number = int(last_receipt.receipt_no.split('/')[-1])  # Extract last sequence number
            new_number = last_number + 1
        else:
            new_number = 1  # Start from 1 if no previous record exists

        # Generate new receipt number
        return f"RCPT-{fy_string}/{new_number:02d}"

    def act_assign_to_wallet(self):
        print('hi')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Students'),
            'res_model': 'op.student',
            # 'domain': [('mobile', 'ilike', self.phone)],
            'context': {
                # 'active_test': self.active,
                'default_amount': self.amount,
            },
            'view_type': 'tree,form',
            'view_mode': 'tree,form',
        }

    amount_in_words = fields.Char(string="Amount in Words", compute="_compute_amount_in_words", store=1)

    @api.depends('amount')
    def _compute_amount_in_words(self):
        print('workssssss')
        for i in self:
            i.amount_in_words = num2words(i.amount, lang='en').upper()

    @api.onchange('reconciliation')
    def _onchange_reconciliation(self):
        if self.reconciliation == True:
            self.reconciliation_date = datetime.now()
        else:
            self.reconciliation_date = False

    def act_print_invoice(self):
        return self.env.ref('fee_collection_17.action_payment_quick_pay_receipt').report_action(self)

    def act_print_with_tax_receipt(self):
        return self.env.ref('fee_collection_17.receipt_with_tax_quick_pay').report_action(self)
