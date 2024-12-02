/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { ListRenderer } from "@web/views/list/list_renderer";
const { onMounted } = owl;
var array = [];
var originalPositions = {};  // Store original positions of rows
var int;

// Patch the ListRenderer template to store and view pinned records
patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");  // For refreshing view
        onMounted(this.pin);
    },
    
    async pin() {
        var current_model = this.props.list.model.env.searchModel.resModel;
        var table_row = $('.o_data_row');
        var row = this.props.list.records;
        
        // Call to fetch pinned records from the server
        var result = await this.orm.call('cp.pin.records', 'pin_record', [current_model]);
        
        if (result) {
            for (var num = 0; num <= table_row.length - 1; num++) {
                if (!row[num]) {
                    console.error('row[' + num + '] is undefined');
                    continue;
                }
                
                var row_id = row[num].resId;
                
                // Store the original position of the rows before pinning
                originalPositions[row_id] = table_row[num].rowIndex;
                
                for (var i = 0; i <= result.length - 1; i++) {
                    array.push({ 'id': result[i].id });
                    
                    if (row_id == result[i].id) {
                        if (row[num].resModel == result[i].model) {
                            table_row[num].style.setProperty('--table-bg', '#C6FED5');
                            table_row[num].parentNode.insertBefore(table_row[num], table_row[0]);  // Move pinned row to the top
                        }
                    }
                }
            }
        }
    },
    
    async pin_record_details(ev, record) {
        var row = $(ev.target).closest('.o_data_row')[0];  // Get the row element
        var num = 0;
        
        // Unpin logic: check if the record is already pinned
        array.forEach((line, index) => {
            if (line.id == record.resId) {
                row.style.setProperty('--table-bg', 'white');  // Reset background color
                int = index;
                num = 1;
            }
        });
        
        // If already pinned, remove from the array and move back to its original position
        if (num == 1) {
            array.splice(int, 1);
            
            // Restore the row to its original position
            // var originalIndex = originalPositions[record.resId];
            // var tableRows = row.parentNode.children;
            
            // Move the row to its original index
            // if (originalIndex !== undefined && originalIndex < tableRows.length) {
            //     row.parentNode.insertBefore(row, tableRows[originalIndex]);
            // }

            // Unpin the record and refresh the list to order by S.No
            this.refreshListView();
        }
        
        // If not pinned, pin the record
        if (num == 0) {
            $($(ev.target).parent().parent().parent()[0]).prepend(row);  // Move to the top
            array.push({ 'id': record.resId });
            row.style.setProperty('--table-bg', '#C6FED5');  // Change background color to indicate pinning
        }
        
        // Save pin/unpin status to the server
        var result = await this.orm.call('cp.pin.records', 'save_pin_record', [[parseInt(record.resId), record.resModel, row.style.backgroundColor]]);
        if (result) {
            // Handle the result if needed
        }
    },
    
    refreshListView() {
        // Refresh the current list view to ensure correct order
        this.action.doAction({
            type: "ir.actions.client",
            tag: "reload",
        });
    },
    
    // Pin header added
    freezeColumnWidths() {
        const table = this.tableRef.el;
        const child_table = table.firstElementChild.firstElementChild;
        const tfoot = table.lastElementChild.firstElementChild;

        // Check if the "S.No" column is already present
        if (!$(child_table).find('.o_list_row_count_sheliya').length) {
	    // Find the index of the multiple select checkbox column
            const selectCheckboxIndex = $(child_table).find('th').index($(child_table).find('.o_list_record_selector').closest('th'));

            if (selectCheckboxIndex !== -1) {
                const pinColumn = '<th class="o_list_row_header o_list_row_pin">Pin</th>';
                $(child_table).find('th').eq(selectCheckboxIndex).after(pinColumn);
            } else {
                $(tfoot).find('td:first-child').remove();
            }
        }

        return super.freezeColumnWidths();
    },
});