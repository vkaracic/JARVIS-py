define([
    'backbone',
    'js/views/queue',
    'js/views/models',
    'js/views/model_details',
    'js/views/new_task',
    'js/views/new_model',
    'js/collections/task_collection',
    'js/collections/models_collection'
], function(Backbone,
            QueueList,
            ModelsView,
            ModelDetailsView,
            NewTaskView,
            NewModelView,
            TaskCollection,
            ModelsCollection) {

    return Backbone.Router.extend({

        root : '/',

        routes: {
            'queue': 'queue',
            'models': 'models',
            'models/:id': 'singleModel',
            'new-task': 'newTask',
            'new-model': 'newModel',
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

        singleModel: function(id) {
            var view = new ModelDetailsView({id: id, el: $('.main-content')});
        },

        newTask: function() {
            var view = new NewTaskView({el: $('.main-content')});
        },

        newModel: function() {
            var view = new NewModelView({el: $('.main-content')});
            view.render();
        },

        start: function () {
            Backbone.history.start();
            return this;
        },
    });
});
