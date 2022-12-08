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
				"doctype": "Shipment at Freight Forwarder",
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
		"Shipment at Freight Forwarder",
		source_name,
		{
			"Shipment at Freight Forwarder": {
				"doctype": "Consolidated Cargo Order",
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Shipment at Freight Details": {
				"doctype": "Consolidated Cargo Order Details",
				"field_map": {
					"name": "consolidated_cargo_order_details",
					"purchase_invoice": "purchase_invoice",
                    "item_id": "item_id",
					"qty":"qty",
					"customs_tariff_number":"customs_tariff_number",
					"received_qty":"received_qty",
					"amount":"amount",
					"base_amount":"base_amount"
				}
			}
		},
		target_doc,
	)

	doc.set_onload("ignore_price_list", True)

	return doc