define([
    'backbone.relational'
    ],
    function() {
        return Backbone.RelationalModel.extend({
            urlRoot: '/api/private/models/',
        });
    }
);
