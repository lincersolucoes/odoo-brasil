# © 2018 Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class l10nBrPaymentStatement(models.Model):
    _name = 'l10n_br.payment.statement'

    _description = "Payment Statement"
    _order = "date desc, id desc"
    _inherit = ['mail.thread']

    @api.one
    @api.depends('journal_id')
    def _compute_currency(self):
        self.currency_id = \
            self.journal_id.currency_id or self.company_id.currency_id

    name = fields.Char(
        string='Reference', states={'open': [('readonly', False)]},
        copy=False, readonly=True)
    date = fields.Date(
        states={'confirm': [('readonly', True)]},
        copy=False, default=fields.Date.context_today)
    end_balance = fields.Monetary(
        'Ending Balance', states={'confirm': [('readonly', True)]},
        currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', compute='_compute_currency', string="Currency")
    state = fields.Selection(
        [('open', 'New'), ('confirm', 'Validated')], string='Status',
        required=True, readonly=True, copy=False, default='open')
    journal_id = fields.Many2one(
        'account.journal', string='Journal', required=True,
        states={'confirm': [('readonly', True)]})
    company_id = fields.Many2one(
        'res.company', related='journal_id.company_id', string='Company',
        store=True, readonly=True)

    line_ids = fields.One2many(
        'l10n_br.payment.statement.line', 'statement_id',
        string='Statement lines', states={'confirm': [('readonly', True)]},
        copy=True)


class l10nBrPaymentStatementLine(models.Model):
    _name = 'l10n_br.payment.statement.line'
    _description = "Bank Statement Line"
    _order = "statement_id desc, date desc, id desc"

    name = fields.Char(string='Label', required=True)
    date = fields.Date()
    amount = fields.Monetary(digits=0, currency_field='journal_currency_id')
    journal_currency_id = fields.Many2one(
        'res.currency', related='statement_id.currency_id',
        help='Utility field to express amount currency', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    statement_id = fields.Many2one(
        'l10n_br.payment.statement', string='Statement',
        index=True, required=True, ondelete='cascade')
    journal_id = fields.Many2one(
        'account.journal', related='statement_id.journal_id',
        string='Journal', store=True, readonly=True)
    ref = fields.Char(string='Reference')
    company_id = fields.Many2one(
        'res.company', related='statement_id.company_id',
        string='Company', store=True, readonly=True)
