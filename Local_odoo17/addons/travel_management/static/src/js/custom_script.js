odoo.define('custom_date_widget', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');

    basic_fields.DateField.include({
        _renderReadonly: function () {
            this._super.apply(this, arguments);
            var currentDate = new Date();
            var fieldDate = new Date(this.value);
            if (fieldDate < currentDate) {
                this.$el.css('visibility', 'hidden');
                // or this.$el.prop('readonly', true); if you want to make it read-only instead
            }
        },
    });
});

