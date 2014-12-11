from openerp import api, fields, models
from openerp.exceptions import ValidationError
from requests.exceptions import HTTPError
import logging

_logger = logging.getLogger(__name__)


def on_dtmf_received(channel, ev):
    try:
        if self.dialer.create_lead_on_key_press and ev.get('digit') == '*':
            _logger.debug('DTMF * press on channel: %s' % channel.get(
                'channelId'))
        else:
            _logger.debug('UNKNOWN DTMF %s RECEIVED' % ev.get('digit'))

    except HTTPError as e:
        # Just ignore errors
        _logger.warn('DTMF RECEIVE ERROR: %s' % str(e))
        _logger.error(format_exception())


class dialer_crm(models.Model):
    _name = 'asterisk.dialer'
    _inherit = 'asterisk.dialer'

    def __init__(self, pool, cr):
        super(dialer_crm, self).__init__(pool, cr)
        handlers = super(dialer_crm, self).get_stasis_event_handlers()
        handlers.append(['ChannelDtmfReceived', on_dtmf_received])
        self.stasis_event_handlers = handlers

    create_lead_on_answer = fields.Boolean(string='Create Lead on Call Answer')
    lead_on_answer_campaign = fields.Selection(
        selection='_get_lead_campaigns',
        string='Answer Lead Campaign')
    lead_on_answer_channel = fields.Selection(
        selection='_get_lead_channels',
        string='Answer Lead Channel')
    lead_on_answer_source = fields.Selection(
        selection='_get_lead_sources',
        string='Answer Lead Source')
    create_lead_on_key_press = fields.Boolean(string='Create Lead on * Press')
    lead_on_key_press_campaign = fields.Selection(
        selection='_get_lead_campaigns',
        string='* Press Lead Campaign')
    lead_on_key_press_channel = fields.Selection(
        selection='_get_lead_channels',
        string='* Press Lead Channel')
    lead_on_key_press_source = fields.Selection(selection='_get_lead_sources',
                                                string='* Press Lead Source')

    @api.onchange('create_lead_on_answer', 'create_lead_on_key_press')
    def _check_crm_is_installed(self):
        try:
            if self.create_lead_on_answer or self.create_lead_on_key_press:
                leads = self.env['crm.lead']
        except KeyError:
            raise ValidationError(
                'CRM module is not installed. Install CRM first.')

    @api.model
    def _get_lead_campaigns(self):
        """
        Fill campaigns selection with existing CRM campaigns.
        """
        return [(c.name, c.name) for c in self.env[
            'crm.tracking.campaign'].search([])]

    @api.model
    def _get_lead_channels(self):
        """
        Fills channels select box with existing CRM channels.
        """
        return [(c.name, c.name) for c in self.env[
            'crm.tracking.medium'].search([])]

    @api.model
    def _get_lead_sources(self):
        """
        Fill sources select box with existing CRM sources.
        """
        return [(c.name, c.name) for c in self.env[
            'crm.tracking.source'].search([])]
