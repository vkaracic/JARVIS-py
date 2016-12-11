define([
        'underscore',
        'underscore.string',
        'backbone',
        'js/collections/models_collection',
        'text!js/templates/new_task.html',
        'js-cookie'
    ], function(_,
                _s,
                Backbone,
                ModelsCollection,
                NewTaskTemplate,
                Cookie) {
    return Backbone.View.extend({
        template: _.template(NewTaskTemplate),

        events: {
            'click .new-task-btn': 'addTask'
        },

        getModel: function(title) {
            return this.collection.where({'title': title})[0];
        },

        addTask: function(e) {
            e.preventDefault();
            this.$('.new-task-btn').attr('disabled', true);
            var data = {
                'training_data_csv_name': this.$('[name=training_data]').val(),
                'min_error': this.$('[name=min_error]').val(),
                'iterations': this.$('[name=iterations]').val()
            };
            this.submitTask(data);
            window.location.href = '/#queue';
        },

        submitTask: function(data) {
            var url = _s.sprintf(
                '/api/private/models/%s/train/',
                this.getModel(this.$('[name=model]').val()).id
            );
            $.ajax({
                url: url,
                method: 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': Cookie.get('csrftoken')
                },
                data: JSON.stringify(data),
                success: function(data) {
                    console.log("SUCCESS!");
                },
                error: function() {
                    console.log('ERROR');
                }
            });
        },

        initialize: function() {
            var self = this;
            this.collection = new ModelsCollection();
            this.collection.fetch().done(function() {
                self.render();
            });
        },

        render: function() {
            this.$el.html(this.template);
            _.each(this.collection.models, function(item) {
                var option = _s.sprintf('<option>%s</option', item.get('title'));
                this.$('select[name=model]').append(option);
            });
        }
    });
});
