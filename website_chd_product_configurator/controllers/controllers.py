# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.osv import orm
import json
import openerp.addons.website_sale.controllers.main as websale


class Chd_website(http.Controller):

    @http.route('/chd_init/', auth='public', website=True)
    # need to append useless **kwargs to allow the openerp debug switch to work.
    def start(self, selected_id = False, type = False, fromshop=False,**kwargs):
        partner = request.env.user.partner_id
        if not partner:
            return request.render(
                'website_chd_product_configurator.no_partner', {})
        product_template_model = request.env['product.template']
        product_type_model = request.env['product.type']
        # when posting a selected product to configure
        if selected_id:
            curr_types = product_type_model.search([
                ('product_option_ids', 'in', [selected_id])
                ])
            # explicitly cast selected id integer otherwise browse raises error
            curr_product = product_template_model.browse([int(selected_id)])
            curr_chd_price_component_ats = curr_product.attribute_template_ids
            avail_accessories = curr_product.chd_accessoire_ids
            return request.render(
                'website_chd_product_configurator.configurator',
                {
                    'curr_product_id': curr_product,
                    'curr_types': curr_types,
                    'curr_chd_price_component_ats':
                    curr_chd_price_component_ats,
                    'avail_accessories': avail_accessories,
                    'ref': request.env.ref,
                    })
        """first iteration, loading the page"""
        return request.render('website_chd_product_configurator.conf_start', {
            'conf_products': product_template_model.search([(
                'chd_origin_product', '=', True)
                ]),
            })

    # shows the options list
    @http.route('/chd_init/<model("product.template"):curr_product_id>/',
         website = True)
    def call_configurator(self, curr_product_id = None, **form_data):
        errormsg = []
        message=[]
        product_template_model = request.env['product.template']
        chd_results_model = request.env['chd.product_configurator.result']
        pc_at_model = request.env[
            'price.component.attribute.template']
        all_accessories = []
        all_attributes = {}
        chd_dict = {
            'origin_product_id': curr_product_id.id,
            'partner_id': request.env.user.partner_id.id,
            'state': 'config',
            'quantity': form_data['quantity']
            }
        # dynamic and fixed size types
        if form_data['product_id_chd_size_type'] == "fixed":
            chd_dict['size_id'] = form_data['size']
            chd_size = request.env['chd.size'].browse([
                int(form_data['size'])
                ])
            chd_dict['width'] = chd_size.width
            chd_dict['height'] = chd_size.height
        else:
            chd_dict['width'] = int(form_data['width'])
            chd_dict['height'] = int(form_data['height'])
        # if there aren't any errors, upload the image
        has_image = product_template_model.browse([
            int(form_data['product_id'])
            ]).chd_configurator_has_image
        if has_image:
            try:
                import base64
                fileitem = form_data['pic']
                # add uploaded image to configurator
                chd_dict['image'] = base64.b64encode(fileitem.stream.read())
                chd_dict['image_filename'] = fileitem.filename
                message.append('image uploaded successfully')
            except:
                message.append('Problems uploading your image, please contact us')
        if not message:
            message.append('no image needed for this product')
        accessory_list = []
        for key in form_data:
            if ('pricecomponent_' in key):
                # if it is of type "string" the value is the index of the
                # selection in pricecomponent_name, the id encoded in the key
                # if it is of type numerical the value is the actual value of
                # the pricecomponent field, the id is encoded in the key
                if ('pricecomponent_string' in key) or ('pricecomponent_int' in key):
                    pricecomponent_id = int(key.split('_')[3])
                    pricecomponent_value = int(form_data[key])
                    # the configurator stores the attributes in a
                    # dictionary in the "attributes" field ,
                    all_attributes.update({
                        '_attribute_%s' %(str(pricecomponent_id)):
                            int(pricecomponent_value)
                        })
                # add accessories to configurator dict
            if ('qtyaccessoryid_' in key):
                # extrapolate the id encoded the name
                accessory_id = int(key.split('_')[1])
                # get the associated value by choosing the field with the
                # right name accessoryid_{id}=on/off and the associated
                # quantity would be qtyaccessoryid_{id}=9898
                if form_data[key]:
                    accessory_qty = int(form_data[key])
                    accessory_list.append((0, 0, {
                        'product_id': accessory_id,
                        'quantity': accessory_qty, }
                        ))
        chd_dict['attributes'] = str(all_attributes)
        if accessory_list:
            chd_dict['accessoire_line_ids'] = accessory_list
        # dictionary is complete, create configurator
        try:
            new_chd = request.env['chd.product_configurator'].create(chd_dict)
        except (orm.except_orm, AssertionError) as e:
            errormsg.append(e.value)
        try:
            res = new_chd._model.calculate_price(
                request.cr, request.uid, [new_chd.id], context=request.context)
            results = chd_results_model.search([
                ('configurator_id', '=', new_chd.id)])
        except orm.except_orm as e:
                errormsg.append(e.value)
        if errormsg:
            product_type_model = request.env['product.type']
            curr_types = product_type_model.search([
                ('product_option_ids', 'in', [int(form_data['product_id'])])
                ])
            avail_accessories = curr_product_id.chd_accessoire_ids
            curr_chd_price_component_ats = curr_product_id.attribute_template_ids.filtered('active')
            return request.render(
                'website_chd_product_configurator.configurator', {
                    'curr_product_id': curr_product_id,
                    'curr_types': curr_types,
                    'avail_accessories': avail_accessories,
                    'curr_chd_price_component_ats':
                    curr_chd_price_component_ats,
                    'errormsg': errormsg,
                    })
        if not message:
            append.message('')
        return request.render(
            'website_chd_product_configurator.sale_options',
            {
                'curr_product_id': curr_product_id,
                'curr_chd': new_chd,
                'all_accessories': all_accessories,
                'results': results,
                'configuration_form': str(form_data),
                'message': message,
                'summary': form_data['summary'],
                })


    @http.route('/chd_init/buy/<model("chd.product_configurator.result"):result>/', website = True)
    def chosen_option(self, result=None, **form_data):
        partner = request.env.user.partner_id
        if not partner:
            return request.render(
                'website_chd_product_configurator.no_partner', {})
        context_for7call = dict(request.context or {}, active_id = result.id)
        fields = [
            'order_id',
            'return_to_order',
            'display_order_id',
            'result_id']
        if form_data['action'] == 'buy':
            #Assign configurator object to sale order of the current cart
            result.configurator_id.order_id = request.website.sale_get_order(force_create=1)
            doorder_model = request.env['chd.product_configurator.do_order']
            # again, access 7.0 with ._model property
            doorder_res = doorder_model._model.default_get(
                request.cr, request.uid,
                fields_list=fields, context=context_for7call)
            #will make all "erased" results point to wishlist 0.
            result.write({
                'wishlist': 0,
                })
            order = request.env['sale.order'].browse(
                [doorder_res['order_id']])
            return request.render(
                'website_chd_product_configurator.buy_option', {
                    'result': result,
                    'order': order,
                    })
