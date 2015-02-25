# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.osv import orm
import openerp.addons.website_sale.controllers.main as websale
from . import controllers as pc


class website_sale_ext(websale.website_sale, pc.Chd_website):

    @http.route()
    def product(self,product):
        if product.chd_origin_product:
                return super(website_sale_ext,self).start(product.id)
        return super(website_sale_ext, self).product(product)


