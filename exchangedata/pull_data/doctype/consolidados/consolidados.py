# Copyright (c) 2022, Muhammad Zubair and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Consolidados(Document):
	@frappe.whitelist()
	def get_data(self, throw_if_missing=False):
		# return self.total
		check = frappe.db.sql(""" select name from `tabPurchase Invoice` where consolidados=%s""",(self.name))
		if check:
			frappe.msgprint('Record Already exists with Purchase Invoice '+ check[0][0])
		else:
			for a in self.consolidated_cargo_order_details:
				pi = frappe.get_doc('Purchase Invoice',a.purchase_invoice)
				pi.consolidados = self.name
				pi.save()
				frappe.msgprint("Purchase Invoice Updated Successfully With "+ self.name)
