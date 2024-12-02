/** @odoo-module */
import { patch } from '@web/core/utils/patch';
import { Field } from "@web/views/fields/field";
import { onWillStart } from '@odoo/owl';
import { useService } from "@web/core/utils/hooks";
import { evaluateBooleanExpr } from "@web/core/py_js/py";


export function fieldVisualFeedback(field, record, fieldName, fieldInfo) {
  const readonly = evaluateBooleanExpr(fieldInfo.readonly, record.evalContextWithVirtualIds);
  const required = evaluateBooleanExpr(fieldInfo.required, record.evalContextWithVirtualIds);
  const inEdit = record.isInEdition;

  let empty = !record.isNew;
  if ("isEmpty" in field) {
      empty = empty && field.isEmpty(record, fieldName);
  } else {
      empty = empty && !record.data[fieldName];
  }
  empty = inEdit ? empty && readonly : empty;
  return {
      readonly,
      required,
      invalid: record.isFieldInvalid(fieldName),
      empty,
  };
} 

patch(Field.prototype, {
    setup() {
    super.setup(...arguments);
    this.required_fields = []
    this.orm = useService("orm")
    this.rpc = useService('rpc');
    onWillStart(async () => {    
                this.custom_required = await this.rpc("/custom/required_fields", {
                              "fieldName": this.props.record.fields[this.props.name]['name'],
                              "model": this.props.record._config.resModel,
                              "company_id": this.props.record._config.currentCompanyId
                });
        });
    },

    get classNames() {
      const { class: _class, fieldInfo, name, record } = this.props;
      const { readonly, required, invalid, empty } = fieldVisualFeedback(
          this.field,
          record,
          name,
          fieldInfo || {}
      );
      const classNames = super.classNames;
      classNames.o_required_modifier = Boolean(this.custom_required) | required;
      return classNames;
  } 
});
