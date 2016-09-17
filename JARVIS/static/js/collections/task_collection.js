define([
    'backbone',
    'js/models/task'
    ],
    function(Backbone, TaskModel) {
        return Backbone.Collection.extend({
            model: TaskModel,
            url: '/api/tasks/'
        });
    }
);
