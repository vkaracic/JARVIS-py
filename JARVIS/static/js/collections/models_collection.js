define([
    'backbone',
    'js/models/model'
    ],
    function(Backbone, ModelModel) {
        return Backbone.Collection.extend({
            model: ModelModel,
            url: '/api/private/models/'
        });
    }
);
