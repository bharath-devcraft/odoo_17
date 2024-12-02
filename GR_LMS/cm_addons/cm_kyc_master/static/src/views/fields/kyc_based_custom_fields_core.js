/** @odoo-module */
import { patch } from '@web/core/utils/patch';
import { Record } from "@web/model/relational_model/record";
import { markup } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { escape } from "@web/core/utils/strings";




patch(Record.prototype, {
  setup() {
    super.setup(...arguments);
  },


  async CustomCheckValidity({ silent, displayNotification } = {}) {
    const unsetRequiredFields = [];
    for (const fieldName in this.activeFields) {
        const fieldType = this.fields[fieldName].type;
        if (this._isInvisible(fieldName) || this.fields[fieldName].relatedPropertyField) {
            continue;
        }
        switch (fieldType) {
            case "boolean":
            case "float":
            case "integer":
            case "monetary":
                continue;
            case "html":
                if (await this.CustomRequired(fieldName) && this.data[fieldName].length === 0) {
                    unsetRequiredFields.push(fieldName);
                }
                break;
            case "one2many":
            case "many2many": {
                const list = this.data[fieldName];
                if (
                    (await this.CustomRequired(fieldName) && !list.count) ||
                    !list.records.every((r) => !r.dirty || r._checkValidity({ silent }))
                ) {
                    unsetRequiredFields.push(fieldName);
                }
                break;
            }
            case "properties": {
              const value = this.data[fieldName];
              if (value) {
                  const ok = value.every(
                      (propertyDefinition) =>
                          propertyDefinition.name &&
                          propertyDefinition.name.length &&
                          propertyDefinition.string &&
                          propertyDefinition.string.length
                  );
                  if (!ok) {
                      unsetRequiredFields.push(fieldName);
                  }
              }
              break;
          }
          case "json": {
              if (
                  await this.CustomRequired(fieldName) &&
                  (!this.data[fieldName] || !Object.keys(this.data[fieldName]).length)
              ) {
                  unsetRequiredFields.push(fieldName);
              }
              break;
          }
          default:
              if (!this.data[fieldName] && await this.CustomRequired(fieldName)) {
                  unsetRequiredFields.push(fieldName);
              }
      }
  }
  if (silent) {
    return !unsetRequiredFields.length;
  }

  for (const fieldName of Array.from(this._unsetRequiredFields)) {
      this._invalidFields.delete(fieldName);
  }
  this._unsetRequiredFields.clear();
  for (const fieldName of unsetRequiredFields) {
      this._unsetRequiredFields.add(fieldName);
      this._setInvalidField(fieldName);
  }
  const isValid = !this._invalidFields.size;
  if (!isValid && displayNotification) {
      const items = [...this._invalidFields].map((fieldName) => {
          return `<li>${escape(this.fields[fieldName].string || fieldName)}</li>`;
      }, this);
      this._closeInvalidFieldsNotification = this.model.notification.add(
          markup(`<ul>${items.join("")}</ul>`),
          {
              title: _t("KYC Mandatory Fields"),
              type: "info",
          }
      );
  }
  return isValid;
  },
  async CustomRequired(fieldName) {
    const custom_required =  await this.model.rpc("/custom/required_fields", {
      "fieldName": fieldName,
      "model": this._config.resModel,
      "company_id": this._config.currentCompanyId
    })
    return custom_required
  },

    async save(options) {
        await this.model._askChanges()
        return this.model.mutex.exec(() => this._save(options)) && this.CustomCheckValidity({ displayNotification: true })
    }	
});
