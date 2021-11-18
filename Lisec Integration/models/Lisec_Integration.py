
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from xml.dom import minidom
import base64
from xml.etree import ElementTree as ET
import xmltodict
import json
class TESTXML(models.TransientModel):
    _name = 'xml.tester'
    xml_file =  fields.Binary(
        string='XML File',
    )
    

    def validate(self):
        # parse an xml file by name
        file_content = base64.decodestring(self.xml_file)
        file_content = file_content.decode("utf-8")
        mydo2c = xmltodict.parse(file_content)
        mydo2c = json.loads(json.dumps(mydo2c))
        mydo2c = dict(mydo2c)
        customer = mydo2c["document"]["order"]["header"]["customer"]["name"]
        cust_name = mydo2c["document"]["order"]["header"]["customer"]["name"]
        cust_phone = mydo2c["document"]["order"]["header"]["customer"]["phone_number"]
        cust_addr = mydo2c["document"]["order"]["header"]["customer"]["title"]
        cust_country = mydo2c["document"]["order"]["header"]["customer"]["country"]
        customer = self.env["res.partner"].search([('name', '=', cust_name)])
        if not customer:
            country_id = self.env["res.country"].sudo().search([('name','=', cust_country)])
            if not country_id:
                country_id = self.env["res.country"].sudo().create({'name': cust_country})
            customer =self.env["res.partner"].create({'name': cust_name, 'mobile': cust_phone, 'street':cust_addr,'country_id': country_id.id, 'customer_rank': 1})

        print("PPPPPPPPP")
        print("PPPPPPPPP")
        print(cust_name)
        print("PPPPPPPPP")
        print(customer)
        print("PPPPPPPPP")
        print("PPPPPPPPP")
        items = mydo2c["document"]["order"]["items"]["item"]
        items_dict = []
        for item in items:
            pr = self.env["product.template"].search([('name', '=', item["item_description"])])
            typ = item["@type"]
            if not pr:
                pr = self.env["product.product"].create({'name': item["item_description"], 'item_type': typ})
                pr = pr.product_tmpl_id

            list_attrs = ["width","height","calculation_area","price_per_sqm_net","unit_weight","unit_price_net"]
            var_val_ids = []
            var_val_ids2 = []
            var_ids = []

            for val in list_attrs:

                pr_attr = self.env["product.attribute"].search([('name', '=', val)])
                if not pr_attr:
                    pr_attr = self.env["product.attribute"].create({'name': val, 'display_type': 'select', 'create_variant': 'dynamic'})
 
                attr_exis_values = pr_attr.value_ids.mapped("name")

                attr_val = item[str(val)]
                if attr_val not in attr_exis_values:
                    pr_Atrr_val = pr_attr.value_ids.create({"attribute_id": pr_attr.id, 'name': attr_val, })
                    # pr_Atrr_val = pr_Atrr_val.name
                    var_val_ids.append(str(pr_Atrr_val.name))
                    var_val_ids2.append(pr_Atrr_val.id)
                else:

                    pr_Atrr_val = pr_attr.value_ids.search([("attribute_id",'=', pr_attr.id) ,('name','=', attr_val)])
                    var_val_ids.append(str(pr_Atrr_val.name))
                    var_val_ids2.append(pr_Atrr_val.id)
                exis_var = pr.attribute_line_ids
                if pr_attr.id not in pr.attribute_line_ids.mapped('attribute_id').ids:
                    self.env["product.template.attribute.line"].sudo().create({'product_tmpl_id': pr.id, 'attribute_id' : pr_attr.id, 'value_ids' : [(6,0,[pr_Atrr_val.id])]})
                else:

                    exis_vals = self.env["product.template.attribute.line"].sudo().search([('product_tmpl_id' ,'=', pr.id), ('attribute_id'  ,'=',  pr_attr.id)])
                    if pr_Atrr_val.id not in exis_vals.value_ids.ids:
                        exis_vals.value_ids = [(4,pr_Atrr_val.id)]
                    
            domain = [('product_tmpl_id', '=', pr.id)]
            for l in var_val_ids:
                domain.append(('product_template_attribute_value_ids', 'ilike', l))
            product = self.env['product.product'].sudo().search(domain)
            if not product:
               product=  self.env["product.product"].sudo().create(
                   {'product_tmpl_id': pr.id, 'product_template_attribute_value_ids': [(6, 0, var_val_ids2)]})
            print("PRRR")
            print("PRRR")
            print("PRRR")
            print(var_val_ids)
            print(product)
            print(item["quantity"]["#text"])
            print("PRRR")
            print("PRRR")
            items_dict.append((0,0,
                {
                    'product_id': product.id,
                    # 'uom': ,
                    'product_uom_qty': float(item["quantity"]["#text"]),
                    'price_unit': float(item["item_price_net"]),
                })
            )
        total_weight = mydo2c["document"]["order"]["order_total_weight"]
        total_sqm = mydo2c["document"]["order"]["order_total_sqm"]
        total_qty = mydo2c["document"]["order"]["order_total_qty"]
        order_number = mydo2c["document"]["order"]["header"]["customer_order_no"]
        project_number = mydo2c["document"]["order"]["header"]["project"]["project_no"]
        project_name = mydo2c["document"]["order"]["header"]["project"]["project_name"]
        delivery_date = mydo2c["document"]["order"]["header"]["delivery_details"]["delivery_date"]
        delivery_type = mydo2c["document"]["order"]["header"]["delivery_details"]["delivery_type"]["#text"]
        currency = mydo2c["document"]["order"]["header"]["currency_code"]
        currency_id = self.env["res.currency"].sudo().search([('name','=', currency)])
        if not currency_id:
            currency_id = self.env["res.currency"].sudo().create({'name': currency})
        price_list_id = self.env["product.pricelist"].sudo().search([('currency_id','=', currency_id.id)])
        if not price_list_id:
            price_list_id = self.env["product.pricelist"].sudo().create({'name': currency +" Pricelist",'currency_id': currency_id.id})
        team = mydo2c["document"]["order"]["header"]["sales_representative2"]["name"]
        team_id = self.env["crm.team"].sudo().search([('name','=', team)])
        if not team_id:
            team_id = self.env["crm.team"].sudo().create({'name': team ,'use_quotations': True})
        user = mydo2c["document"]["order"]["header"]["sales_representative"]["name"]
        user_id = self.env["res.users"].sudo().search([('name','=', user)])
        if not user_id:
            user_id = self.env["res.users"].sudo().create({'name': user ,'login': user.replace(" ", "_")})
        user2 = mydo2c["document"]["order"]["header"]["user_name"]
        user_id2 = self.env["res.users"].sudo().search([('name','=', user2)])
        if not user_id2:
            user_id2 = self.env["res.users"].sudo().create({'name': user2 ,'login': user2.replace(" ", "_")})
        team_id.member_ids = [(4,user_id.id)]
        sale_order = self.env["sale.order"].create({
            'partner_id' : customer.id,
            'order_line': items_dict,
            'total_weight': total_weight,
            'total_sqm': total_sqm,
            'total_qty': total_qty,
            'order_number': order_number,
            'project_number': project_number,
            'project_name': project_name,
            'delivery_type': delivery_type,
            'delivery_date': datetime.strptime(delivery_date,"%Y/%m/%d"),
            'pricelist_id': price_list_id.id,
            'team_id': team_id.id,
            'user_id': user_id.id,
            'order_create_user': user_id2.id,
            })

