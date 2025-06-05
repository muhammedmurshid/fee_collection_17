from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError, UserError


class FeeCollection(models.Model):
    _name = 'admission.fee.collection'
    _description = 'Fee Collection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'

    name = fields.Many2one('logic.students', string='Student Name', required=True)
    batch_id = fields.Many2one('logic.base.batch', string='Batch', required=True, related='name.batch_id', readonly=False)
    mobile_number = fields.Char(string='Mobile Number', related='name.phone_number', readonly=False)
    email = fields.Char(string='Email', related='name.email', readonly=False)
    admission_officer_id = fields.Many2one('res.users', string='Admission Officer',
                                           compute='_compute_get_student_adm_officer', store=True)
    payment_mode = fields.Selection([('cash', 'Cash'), ('cheque', 'Cheque'), ('online', 'Online')],
                                    string='Payment Mode', )
    admission_id = fields.Char(string='Admission No')
    admission_fee = fields.Float(string='Admission Fee', compute='_onchange_batch_id', store=True, )
    paid_amount = fields.Float(string='Paid Amount')
    invoice_date = fields.Date(string='Invoice Date', required=True, default=fields.Date.today())
    payment_reference = fields.Char(string='Payment Reference')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    amount_cgst = fields.Float(string='CGST', compute='_compute_amount_cgst', store=True)
    amount_sgst = fields.Float(string='SGST', compute='_compute_amount_sgst', store=True)
    amount_gst = fields.Float(string='GST', compute='_compute_amount_gst', store=True)
    state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid'), ('credit_note', 'Credit Note')], default='draft', string='Status')
    pending_amt_student = fields.Float(string='Pending Amount', compute='_compute_pending_amount', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    reference_no = fields.Char(string='Payment SI Number', required=True,
                               readonly=False, default=lambda self: _('New'))
    cheque_number = fields.Char(string='Cheque No / Reference No')
    lead_id = fields.Integer('Lead ID')
    admission_date = fields.Date(string='Admission Date', default=fields.Date.today())
