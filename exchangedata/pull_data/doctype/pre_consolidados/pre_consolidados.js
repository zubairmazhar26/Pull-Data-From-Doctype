// Copyright (c) 2022, Muhammad Zubair and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pre-Consolidados', {
	refresh: function(frm) {
		frm.events.add_custom_buttons(frm);
	},
	add_custom_buttons: function(frm) {
		if (frm.doc.docstatus == 0) {
			frm.add_custom_button(__('Purchase Invoice'), function () {
				if (!frm.doc.supplier) {
					frappe.throw({
						title: __("Mandatory"),
						message: __("Please Select a Supplier")
					});
				}
				erpnext.utils.map_current_doc({
					method: "exchangedata.api.make_purchase_receipt",
					source_doctype: "Purchase Invoice",
					target: frm,
					setters: {
						supplier: frm.doc.supplier,
					},
					get_query_filters: {
						docstatus: 1,
						per_received: ["<", 100],
						company: frm.doc.company
					}
				})
			}, __("Get Items From"));
		}
	}
});
