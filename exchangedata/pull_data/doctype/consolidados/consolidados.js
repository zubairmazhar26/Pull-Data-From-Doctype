// Copyright (c) 2022, Muhammad Zubair and contributors
// For license information, please see license.txt

frappe.ui.form.on('Consolidados', {
	refresh: function(frm) {
		frm.events.add_custom_buttons(frm);
		if (frm.doc.total > 0) {
			frm.add_custom_button(__("Asignar a PI"), function() {
				frm.call('get_data', { throw_if_missing: true })
				.then(r => {
					if (r.message) {
						console.log("Data", r.message)
						// do something with linked_doc
					}
				})

			})
		}else {}
	},
	add_custom_buttons: function(frm) {
		if (frm.doc.docstatus == 0) {
			frm.add_custom_button(__('Pre Consolidados'), function () {
				if (!frm.doc.supplier) {
					frappe.throw({
						title: __("Mandatory"),
						message: __("Please Select a Supplier")
					});
				}
				erpnext.utils.map_current_doc({
					method: "exchangedata.api.make_consolidated_cargo",
					source_doctype: "Pre-Consolidados",
					target: frm,
					setters: {
						supplier: frm.doc.supplier,
						shipment_status:'Recibido Miami'
					},
					get_query_filters: {
						docstatus: 0,
						company: frm.doc.company
					}
				})
			}, __("Get Items From"));
		}
	}
});
