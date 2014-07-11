# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Andre@ (<a.gallina@cgsoftware.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from tools.translate import _


class crm_phonecall(osv.osv):

    _inherit = "crm.phonecall"

    def action_phonecall_send_mail(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email
        '''
        assert len(ids) == 1, 'This option should only be \
                               used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            compose_form_id = ir_model_data.get_object_reference(
                cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        phonecall = self.browse(cr, uid, ids, context)[0]
        ctx = dict(context)
        body = phonecall.name + ' '
        body += phonecall.description or ' '
        subject = 'Chiamata del '
        subject +=  phonecall.date or ' '
        ctx.update({
            'default_model': 'crm.phonecall',
            'default_res_id': ids[0],
            'default_partner_ids': [phonecall.user_id.partner_id.id],
            'default_body': body,
            'default_subject': subject,
            'mark_so_as_sent': True,
            'default_state': 'outgoing',
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
