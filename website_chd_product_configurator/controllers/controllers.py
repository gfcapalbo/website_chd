# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.osv import orm
import json


class Chd_website(http.Controller):

    @http.route('/chd_init/', auth='public', website=True)
    # need to append useless **kwargs to allow the openerp debug switch to work.
    def start(self, selected_id = False, type = False, **kwargs):
        partner = request.env.user.partner_id
        if not partner:
            return request.render(
                'website_chd_product_configurator.no_partner', {})
        product_template_model = request.env['product.template']
        product_product_model = request.env['product.product']
        pc_at_model = request.env[
            'price.component.attribute.template']
        product_type_model = request.env['product.type']
        chd_finishing = request.env['product.finishing']
        # when posting a selected product to configure
        if selected_id:
            curr_types = product_type_model.search([
                ('product_option_ids', 'in', [selected_id])
                ])
            # explicitly cast selected id integer otherwise browse raises error
            curr_product = product_template_model.browse([int(selected_id)])
            curr_chd_price_component_ats = curr_product.attribute_template_ids
            avail_accessories = product_product_model.browse(
                curr_product.chd_accessoire_ids.ids)
            return request.render(
                'website_chd_product_configurator.configurator',
                {
                    'curr_product_id': curr_product,
                    'curr_types': curr_types,
                    'curr_chd_price_component_ats':
                    curr_chd_price_component_ats,
                    'avail_accessories': avail_accessories,
                    })
        """first iteration, loading the page"""
        return request.render('website_chd_product_configurator.conf_start', {
            'conf_products': product_template_model.search([(
                'chd_origin_product', '=', True)
                ]),
            })

    # shows the options list
    @http.route('/chd_init/<int:id>/', website = True)
    def call_configurator(self, id = None, **form_data):
        errormsg = ""
        product_template_model = request.env['product.template']
        chd_results_model = request.env['chd.product_configurator.result']
        curr_product_id = product_template_model.browse([id])
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
            chd_dict['width'] = form_data['width']
            chd_dict['height'] = form_data['height']
        # if there aren't any errors, upload the image
        message = ''
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
                message = 'image uploaded successfully'
            except:
                message = 'Problems uploading your image, please contact us'
        if message == '':
            message = 'no image needed for this product'
        for key in form_data:
            if ('pricecomponent_' in key):
                # if it is of type "string" the value is the index of the
                # selection in pricecomponent_name, the id encoded in the key
                # if it is of type numerical the value is the actual value of
                # the pricecomponent field, the id is encoded in the key
                if ('pricecomponent_string' in key) or ('pricecomponent_int' in key):
                    pricecomponent_id = int(key.split('_')[3])
                    pricecomponent_value = form_data[key]
                # the configurator stores the attributes in a
                # dictionary in the "attributes" field ,
                all_attributes[
                    '_attribute_' + str(pricecomponent_id)
                    ] = int(pricecomponent_value)

        # add attributes to the configurator
        chd_dict['attributes'] = str(all_attributes)
        # dictionary is complete, create configurator
        try:
            new_chd = request.env['chd.product_configurator'].create(chd_dict)
        except orm.except_orm as e:
            errormsg = e.value
        except AssertionError as a:
            errormsg = a.value
        # add accessories and price components selections to the configurator
        list = []
        for key in form_data:
            # get only accessories that have been checked
            if ('accessoryid_' in key) and form_data[key] != 0:
                # extrapolate the id encoded the name
                accessory_id = int(key.split('_')[1])
                # get the associated value by choosing the field with the
                # right name accessoryid_{id}=on/off and the associated
                # quantity would be qtyaccessoryid_{id}=9898
                accessory_qty = int(form_data[key])
                list.append((0, 0, {
                    'product_id': accessory_id,
                    'configurator_id': new_chd.id,
                    'quantity': accessory_qty, }
                    ))

        new_chd.write({'accessoire_line_ids':list})
        # oduct configurator is ready, we can now calculate options
        # model refers to old API model, self.pool
        # is not available in controller context (praise the lord for Holger!)
        try:
            res = new_chd._model.calculate_price(
                request.cr, request.uid, [new_chd.id], context=request.context)
            results = chd_results_model.search([
                ('configurator_id', '=', new_chd.id)])
        except orm.except_orm as e:
                errormsg += e.value

        if errormsg != "":
            product_type_model = request.env['product.type']
            product_product_model = request.env['product.product']
            curr_types = product_type_model.search([
                ('product_option_ids', 'in', [int(form_data['product_id'])])
                ])
            avail_accessories = product_product_model.search(
                [('id', 'in', curr_product_id.chd_accessoire_ids.ids)])
            curr_chd_price_component_ats = pc_at_model.search(
                [
                    ('id', 'in', curr_product_id.attribute_template_ids.ids),
                    ('active', '=', True)
                    ])
            return request.render(
                'website_chd_product_configurator.configurator', {
                    'curr_product_id': curr_product_id,
                    'curr_types': curr_types,
                    'avail_accessories': avail_accessories,
                    'curr_chd_price_component_ats':
                    curr_chd_price_component_ats,
                    'errormsg': errormsg,
                    })

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


    @http.route('/chd_init/buy<int:id>/', website = True)
    def chosen_option(self, id = None, **form_data):
        partner = request.env.user.partner_id
        if not partner:
            return request.render(
                'website_chd_product_configurator.no_partner', {})
        result_model = request.env['chd.product_configurator.result']
        result = result_model.browse([id])
        configurator = result.configurator_id.id
        context_for7call = dict(request.context or {}, active_id = result.id)
        fields = [
            'order_id',
            'return_to_order',
            'display_order_id',
            'result_id']
        if form_data['action'] == 'buy':
            doorder_model = request.env['chd.product_configurator.do_order']
            # again, access 7.0 with ._model property
            doorder_res = doorder_model._model.default_get(
                request.cr, request.uid,
                fields_list = fields, context = context_for7call)
            #will make all "erased" results point to wishlist 0.
            result.write({
                'wishlist': 0,
                })
            order = request.env['sale.order'].browse(
                [doorder_res['order_id']])
            return request.render(
                'website_chd_product_configurator.buy_option', {
                    'summary': result.summary,
                    'result': result,
                    'order': order,
                    })

    # method for fetching finishing options via json
    @http.route('/chd_init/getch/', type='json')
    def tr(self, type_id):
        curr_types = request.env['product.finishing'].search(
            [('type_option_ids', 'in', [type_id])])
        data = json.dumps(request.registry['product.finishing'].search_read(
            request.cr,
            request.uid,
            fields=['id', 'name'],
            limit=30,
            domain=[('type_option_ids', 'in', [int(type_id)])],
            context=request.context
            ))
        return data
