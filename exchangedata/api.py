import frappe
from frappe import _, throw
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate



@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) - flt(obj.received_qty)
		target.received_qty = flt(obj.qty) - flt(obj.received_qty)
		target.stock_qty = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.conversion_factor)
		target.amount = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
		target.base_amount = (
			(flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate) * flt(source_parent.conversion_rate)
		)

	doc = get_mapped_doc(
		"Purchase Invoice",
		source_name,
		{
			"Purchase Invoice": {
				"doctype": "pre_consolidados",
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Purchase Invoice Item": {
				"doctype": "Shipment at Freight Details",
				"field_map": {
					"name": "purchase_invoice_item",
					"parent": "purchase_invoice",
                    "item_code": "item_id",
					"customs_tariff_number":"customs_tariff_number",
					"bom": "bom",
					"material_request": "material_request",
					"material_request_item": "material_request_item",
				},
				"postprocess": update_item,
				"condition": lambda doc: abs(doc.received_qty) < abs(doc.qty),
			}
		},
		target_doc,
	)

	doc.set_onload("ignore_price_list", True)

	return doc



@frappe.whitelist()
def make_consolidated_cargo(source_name, target_doc=None):
	doc = get_mapped_doc(
		"Pre-Consolidados",
		source_name,
		{
			"Pre-Consolidados": {
				"doctype": "Consolidados",
				"validation": {
					"docstatus": ["=", 0],
				},
			},
			"Shipment at Freight Details": {
				"doctype": "Consolidated Cargo Order Details",
				"field_map": {
					"name": "consolidated_cargo_order_details",
					"purchase_invoice": "purchase_invoice",
					"customs_tariff_number":"customs_tariff_number",
					"received_qty":"received_qty"
				}
			}
		},
		target_doc,
	)

	doc.set_onload("ignore_price_list", True)

	return doc
@frappe.whitelist()
def get_terrif(iname):
	list1 = []
	it = frappe.db.sql(""" select customs_tariff_number,mineco_mi from `tabItem` where name=%s """,(iname))
	if it:
		list1 = [it[0][0],it[0][1]]
	return list1