# -*- coding: utf-8 -*-
from odoo import http
import json

FIELDS_DATABANK = 'fields.databank'

class FieldsDatabank(http.Controller):

    def _label_name_mismatched(self, ir_model_fields=None, fields_databank_object=None):
        label_name_mismatched = {}
        for ir_fields in ir_model_fields:
                field_name = fields_databank_object.search([('name', '=', ir_fields.name), ('model', '=', FIELDS_DATABANK)])
                model_obj = http.request.env[ir_fields.model]
                if field_name and model_obj._fields[ir_fields.name].args and not model_obj._fields[ir_fields.name].args.get('c_rule'):
                    field_label = fields_databank_object.search([('field_description', '=', ir_fields.field_description),
                                     ('model', '=', FIELDS_DATABANK), ('name', '=', ir_fields.name)])
                    if not field_label:
                        if ir_fields.model in label_name_mismatched.keys():
                            label_name_mismatched[ir_fields.model].append(ir_fields.name)
                        else:
                            label_name_mismatched.update({ir_fields.model : [ir_fields.name]})
        return label_name_mismatched

    def _untracked_attrs(self, ir_model_fields=None, fields_databank_object=None, attrs_keys=None):
        untracked_attrs = {}
        for attrs_key in attrs_keys:
            for ir_fields in ir_model_fields:
                field_name = fields_databank_object.search([('name', '=', ir_fields.name), ('model', '=', FIELDS_DATABANK)])
                model_obj = http.request.env[ir_fields.model]
                fd_object = http.request.env[FIELDS_DATABANK]
                if field_name and model_obj._fields[ir_fields.name].args and not model_obj._fields[ir_fields.name].args.get('c_rule'):
                    if fd_object._fields[ir_fields.name].args and fd_object._fields[ir_fields.name].args.get(attrs_key):
                        if model_obj._fields[ir_fields.name].args and not model_obj._fields[ir_fields.name].args.get(attrs_key):
                            if ir_fields.model in untracked_attrs.keys():
                                untracked_attrs[ir_fields.model] = { f"{ir_fields.name}": f"Add {attrs_key} in FD."}
                            else:
                                untracked_attrs.update({ir_fields.model : { f"{ir_fields.name}" : f"Add {attrs_key} in FD."}})
                        else:
                            if model_obj._fields[ir_fields.name].args.get(attrs_key) != fd_object._fields[ir_fields.name].args.get(attrs_key):
                                if ir_fields.model in untracked_attrs.keys():
                                    untracked_attrs[ir_fields.model].update({f"{ ir_fields.name}\
                                         -> Refactor ({attrs_key}={model_obj._fields[ir_fields.name].args.get(attrs_key)})":\
                                            f"{attrs_key}={fd_object._fields[ir_fields.name].args.get(attrs_key)}"})
                                else:
                                    untracked_attrs.update({ir_fields.model : {f"{ ir_fields.name}\
                                        -> Refactor ({attrs_key}={model_obj._fields[ir_fields.name].args.get(attrs_key)})":\
                                            f"{attrs_key}={fd_object._fields[ir_fields.name].args.get(attrs_key)}"}})
                    else:
                        if model_obj._fields[ir_fields.name].args and model_obj._fields[ir_fields.name].args.get(attrs_key):
                            if ir_fields.model in untracked_attrs.keys():
                                untracked_attrs[ir_fields.model] = { f"{ir_fields.name}": f"Remove the {attrs_key} attribute or add in FD."}
                            else:
                                untracked_attrs.update({ir_fields.model : { f"{ir_fields.name}" : f"Remove the {attrs_key} attribute or add in FD."}})

        return untracked_attrs

    def _fields_type_mismatched(self, ir_model_fields=None, fields_databank_object=None):
        fields_type_mismatched = {}
        for ir_fields in ir_model_fields:
                field_name = fields_databank_object.search([('name', '=', ir_fields.name), ('model', '=', FIELDS_DATABANK)])
                model_obj = http.request.env[ir_fields.model]
                if field_name and model_obj._fields[ir_fields.name].args and not model_obj._fields[ir_fields.name].args.get('c_rule'):
                    fields_type = fields_databank_object.search([('ttype', '=', ir_fields.ttype),
                                     ('model', '=', FIELDS_DATABANK),('name', '=', ir_fields.name)])
                    if not fields_type:
                        if ir_fields.model in fields_type_mismatched.keys():
                            fields_type_mismatched[ir_fields.model].update({ir_fields.name : ir_fields.ttype})
                        else:
                            fields_type_mismatched.update({ir_fields.model : {ir_fields.name : ir_fields.ttype}})
        return fields_type_mismatched
                                     
    def _untracked_fields(self, ir_model_fields=None, fields_databank_object=None):
        untracked_fields = {}
        for ir_fields in ir_model_fields:
                field_name = fields_databank_object.search([('name', '=', ir_fields.name), ('model', '=', FIELDS_DATABANK)])
                model_obj = http.request.env[ir_fields.model]
                if not field_name and model_obj._fields[ir_fields.name].args and not model_obj._fields[ir_fields.name].args.get('c_rule'):
                    if ir_fields.model in untracked_fields.keys():
                        untracked_fields[ir_fields.model].append(ir_fields.name)
                    else:
                        untracked_fields.update({ir_fields.model : [ir_fields.name]})
        return untracked_fields
                                    
    def _grab_kg_models(self, attrs=False):
        avoided_models = ['cm_base_inherit', 'cm_login_page','cm_user_mgmt','fields_databank']
        target_models = [ir_model.model.replace(".", "_") for ir_model in http.request.env['ir.model'].search([
                ('transient', '=', False),('model', 'in', [ir_module_module.name.replace("_", ".")
                         for ir_module_module in http.request.env['ir.module.module'].search([
                                ('category_id', 'in', [ir_module_category.id 
                                for ir_module_category in http.request.env['ir.module.category'].search([
                                        ('name', '=', "custom_modules"),('parent_id', 'in', [ir_module_category.id 
                                        for ir_module_category in http.request.env['ir.module.category'].search([
                                                ('name', '=', "Catalyst")]) if not ir_module_category.create_uid])]) 
                                                if not ir_module_category.create_uid])])
                                                    if ir_module_module.name not in avoided_models])])]
        ir_model_fields = [field_obj for field_obj in http.request.env['ir.model.fields'].search([]) if field_obj.modules in target_models]
        fields_databank_object = http.request.env['ir.model.fields'].search([('model', '=', FIELDS_DATABANK)])
        untracked_fields = self._untracked_fields(ir_model_fields, fields_databank_object)
        untracked_fields_type = self._fields_type_mismatched(ir_model_fields, fields_databank_object)
        untracked_fields_label_name = self._label_name_mismatched(ir_model_fields, fields_databank_object)
        if attrs:
            untracked_attrs = self._untracked_attrs(ir_model_fields, fields_databank_object, ['size', 'copied', 'tracking', 'index', 'copy'])
            return json.dumps({"attributes": untracked_attrs})
        if not attrs:
            return json.dumps({
                 "untracked-fields" : untracked_fields,
                 "untracked-fields-label-name": untracked_fields_label_name,
                 "untracked-fields-type" : untracked_fields_type
                 })

    @http.route('/fields_databank/details', auth='public')
    def fields_tacker(self, **kw):
        return self._grab_kg_models(attrs=False)

    @http.route('/fields_databank/attrs-details', auth='public')
    def fields_attrs_tacker(self, **kw):
        return self._grab_kg_models(attrs=True)
