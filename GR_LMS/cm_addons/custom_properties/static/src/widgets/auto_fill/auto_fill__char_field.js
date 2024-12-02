/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { archParseBoolean } from "@web/views/utils";
import { formatChar } from "@web/views/fields/formatters";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { TranslationButton } from "@web/views/fields/translation_button";
import { useDynamicPlaceholder } from "@web/views/fields/dynamic_placeholder_hook";
import { Component, useExternalListener, useRef, useEffect, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";

export class CharField extends Component {
    static template = "case_sensitive_widget.Auto_Fill_CharField";
    static components = {
        TranslationButton,
    };
    static props = {
        ...standardFieldProps,
        autocomplete: { type: String, optional: true },
        isPassword: { type: Boolean, optional: true },
        placeholder: { type: String, optional: true },
        dynamicPlaceholder: { type: Boolean, optional: true },
        dynamicPlaceholderModelReferenceField: { type: String, optional: true },
    };
    static defaultProps = { dynamicPlaceholder: false };

    setup() {
        this.input = useRef("input");
        this.orm = useService("orm");
        this.allowedSpecialChars = '';
        this.fetchAllowedSpecialChars();
        this.state = useState({
                        errorMessage: '',
                        showError: false,
                    });
        if (this.props.dynamicPlaceholder) {
            const dynamicPlaceholder = useDynamicPlaceholder(this.input);
            useExternalListener(document, "keydown", dynamicPlaceholder.onKeydown);
            useEffect(() =>
                dynamicPlaceholder.updateModel(this.props.dynamicPlaceholderModelReferenceField)
            );
        }
        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            parse: (v) => this.parse(v),
        });
        
    }
    
    
    // Fetch allowed characters from res.config
    async fetchAllowedSpecialChars() {
        try {
            this.allowedSpecialChars = await this.orm.call("custom.properties", "retrieve_allowed_char");
            this.render();
        } catch (error) {
            console.error('Error fetching allowed special characters:', error);
        }
    }
    
    // Construct allowed characters regex
    constructAllowedCharsRegex() {
        let allowedChars = /[a-zA-Z0-9 ]/;
        if (this.allowedSpecialChars) {
            allowedChars = new RegExp(`[${this.allowedSpecialChars}\\w ]`);
        }
        return allowedChars;
    }
    
    
    
    showErrorMessage(message) {
        this.state.errorMessage = message;
        this.state.showError = true;
        setTimeout(() => {
            this.state.showError = false;
            this.render();
        }, 7000); // 7 seconds
    }
    
    onInputChange(ev) {
        var value = ev.target.value;
        console.log("ssssssssssssssssssssssssssssss1",value, this.props.record._config.resId)
        const input = ev.target;
        var model = this.env.model.env.searchModel.resModel
        var rec_id = this.props.record._config.resId || ""
        var self=this;
        var values = this.__owl__.props.record._config.fields
        for (const key in values) {
          if (values.hasOwnProperty(key)) {
            if (values[key].name == this.props.name){
                this.props.type = values[key].type
            }
          }
        }
        if (this.props.type === "char") {
            
            let p = input.selectionStart;
            const allowedRegex = new RegExp(`[^a-zA-Z0-9${this.allowedSpecialChars} ]`, 'g');
            if (input.value.replace(allowedRegex, '') !== input.value) {
                this.showErrorMessage('Special characters is not allowed');
            }
            let newValue = input.value.replace(allowedRegex, '');
            input.value = newValue;
            input.setSelectionRange(p, p);
        }
        
        if(this.props.type === "char") {
            const allowedRegex = new RegExp(`[^a-zA-Z0-9${this.allowedSpecialChars} ]`, 'g');
            this.env.model.rpc('/matching/records',{
                    model: model,
                    field: this.props.name,
                    value: value.replace(allowedRegex, ''),
                    id: rec_id,
                })
                .then(function(result) {
                    if(result.length > 0) {
                        self.input.el.nextSibling.style.display = 'block';
                        var table = self.input.el.nextSibling;
                        $(table).find('tr').remove();
                        var i;
                        for(i = 0; i < result.length; i++) {
                            var row = table.insertRow(i);
                            var cell = row.insertCell(0);
                            cell.innerHTML = result[i];
                        }
                    } else {
                        self.input.el.nextSibling.style.display = 'none';;
                    }
                });
        } else {
            this.env.model.dialog.add(AlertDialog, {
                body: _t("Only Supported for 'char' type please change field type to 'char'"),
            });
            return false;
        }
}


    onBlur(event) {
    if (!event || !event.target) {
        console.error("Event or event.target is undefined");
        return; 
        }
     this.input.el.nextSibling.style.display = 'none';;
        
    }
    

    get shouldTrim() {
        return this.props.record.fields[this.props.name].trim && !this.props.isPassword;
    }
    get maxLength() {
        return this.props.record.fields[this.props.name].size;
    }
    get isTranslatable() {
        return this.props.record.fields[this.props.name].translate;
    }
    get formattedValue() {
        return formatChar(this.props.record.data[this.props.name], {
            isPassword: this.props.isPassword,
        });
    }

    parse(value) {
        if (this.shouldTrim) {
            return value.trim();
        }
        return value;
    }
}

export const charField = {
    component: CharField,
    displayName: _t("Text"),
    supportedTypes: ["char"],
    supportedOptions: [
        {
            label: _t("Dynamic placeholder"),
            name: "dynamic_placeholder",
            type: "boolean",
            help: _t("Enable this option to allow the input to display a dynamic placeholder."),
        },
        {
            label: _t("Model reference field"),
            name: "dynamic_placeholder_model_reference_field",
            type: "field",
            availableTypes: ["char"],
        },
    ],
    extractProps: ({ attrs, options }) => ({
        isPassword: archParseBoolean(attrs.password),
        dynamicPlaceholder: options.dynamic_placeholder || false,
        dynamicPlaceholderModelReferenceField:
            options.dynamic_placeholder_model_reference_field || "",
        autocomplete: attrs.autocomplete,
        placeholder: attrs.placeholder,
    }),
};

registry.category("fields").add("auto_fill_1", charField);
