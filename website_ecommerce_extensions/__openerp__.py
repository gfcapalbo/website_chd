# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013,14 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

{
    'name': "website_ecommerce_extensions",
    'description': '',
    'summary': 'Extensions and oimprovements for ecommerce module',
    'category':'Website',
    'website': 'www.therp.nl',
    'author' : 'Therp B.V.',
    'version': '8.0.01',
    'depends': [
                'website',
		        'website_sale',
                'chd_product_configurator',
               ],
    'data': [
            'templates/templates.xml',
            ],
        'installable': True,
        'application': True,
}
