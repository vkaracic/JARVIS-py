define([
    'backbone',
    'js/views/queue',
    'js/views/models',
    'js/collections/task_collection',
    'js/collections/models_collection'
], function(Backbone,
            QueueList,
            ModelsView,
            TaskCollection,
            ModelsCollection) {

    return Backbone.Router.extend({

        root : '/',

        routes: {
            'queue': 'queue',
            'models': 'models'
        },

        queue: function() {
            var collection = new TaskCollection(),
                queue = new QueueList({collection: collection, el: $('.main-content')});
            queue.render();
        },

        models: function() {
            var collection = new ModelsCollection(),
                view = new ModelsView({collection: collection, el: $('.main-content')});
            view.render();
        },

        start: function () {
            Backbone.history.start();
            return this;
        },
    });
});
