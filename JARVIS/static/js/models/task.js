define([
    'backbone.relational'
    ],
    function() {
        return Backbone.Model.extend({
            urlRoot: '/api/tasks/',
        });
    }
);
