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

export class CharOnlyField extends Component {
    static template = "char_only_widget.CharOnlyField";
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

    showErrorMessage(message) {
        this.state.errorMessage = message;
        this.state.showError = true;
        setTimeout(() => {
            this.state.showError = false;
            this.render();
        }, 7000);
    }

    onInputChange(event) {
        const input = event.target;
        let p = input.selectionStart;

        // Validate input: only alphabets (A-Z, a-z) and spaces allowed
        if (input.value.replace(/[^A-Za-z\s]/g, '') !== input.value) {
            this.showErrorMessage('Only alphabets are allowed!');
        }

        let newValue = input.value.replace(/[^A-Za-z\s]/g, '');
        input.value = newValue;
        input.setSelectionRange(p, p);
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

export const charOnlyField = {
    component: CharOnlyField,
    displayName: _t("Alphabets Only"),
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

registry.category("fields").add("char_only", charOnlyField);
