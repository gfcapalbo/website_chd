# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.osv import orm
import openerp.addons.website_sale.controllers.main as websale
from telnetlib import theNULL



class website_sale_ext(websale.website_sale):

    @http.route()
    def product(self,product):
        if product.chd_origin_product:
                from . import controllers as pc
                configurator = pc.Chd_website()
                return pc.Chd_website.start(configurator,product.id)
        return super(website_sale_ext, self).product(product)




    def checkout_values(self, data=None):
        values_sender={}
        if data and data['use_sender_address']=="-1" :
            values_sender['use_sender_address']=True
            values_sender['sender_name'] = data['sender_name']
            values_sender['sender_contact'] = data['sender_contact']
            values_sender['sender_street'] = data['sender_street']
            values_sender['sender_zip'] = data['sender_zip']
            values_sender['sender_city'] = data['sender_city']
            values_sender['sender_phone'] = data['sender_phone']
            values_sender['sender_email'] = data['sender_email']
            order = request.website.sale_get_order(force_create=1, context=None)
            order.write(values_sender)
        return super(website_sale_ext, self).checkout_values(data)





