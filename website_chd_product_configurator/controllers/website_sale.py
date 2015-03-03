# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.osv import orm
import openerp.addons.website_sale.controllers.main as websale



class website_sale_ext(websale.website_sale):

    @http.route()
    def product(self,product):
        if product.chd_origin_product:
                from . import controllers as pc
                configurator = pc.Chd_website()
                return pc.Chd_website.start(configurator,product.id)
        return super(website_sale_ext, self).product(product)


