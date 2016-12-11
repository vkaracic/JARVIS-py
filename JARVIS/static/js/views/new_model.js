define([
        'underscore',
        'underscore.string',
        'backbone',
        'js/collections/models_collection',
        'text!js/templates/new_model.html',
        'js-cookie'
    ], function(_,
                _s,
                Backbone,
                ModelsCollection,
                NewModelTemplate,
                Cookie) {
    return Backbone.View.extend({
        template: _.template(NewModelTemplate),

        events: {
            'click .new-model-btn': 'addModel'
        },

        addModel: function(e) {
            e.preventDefault();
            this.$('.new-model-btn').attr('disabled', true);
            var data = {
                'title': this.$('[name=title]').val(),
                'num_inputs': this.$('[name=num_inputs]').val(),
                'num_hidden': this.$('[name=num_hidden]').val(),
                'num_outputs': this.$('[name=num_outputs]').val(),
                'learning_rate': this.$('[name=learning_rate]').val(),
                'cost': this.$('[name=cost]').val(),
                'optimizer': this.$('[name=optimizer]').val(),
                'activation': this.$('[name=activation]').val(),
                'permission_type': this.getPermissionType(this.$('[name=permission_type]').val()),
            };
            this.submitModel(data);
            window.location.href = '/#models';
        },

        getPermissionType: function(perm) {
            if (perm === 'Free use') {
                return 0;
            } else if (perm === 'Only me') {
                return 1;
            } else if (perm === 'Only my team') {
                return 2;
            }
        },

        submitModel: function(data) {
            $.ajax({
                url: '/api/private/models/',
                method: 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': Cookie.get('csrftoken')
                },
                data: JSON.stringify(data),
                success: function() {
                    console.log("SUCCESS!");
                },
                error: function() {
                    console.log('ERROR');
                }
            });
        },

        initialize: function() {

        },

        render: function() {
            this.$el.html(this.template);
        }
    });
});