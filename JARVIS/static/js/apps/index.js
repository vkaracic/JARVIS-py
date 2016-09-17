require([
        'backbone',
        'js/routers/index',
    ],
    function(
        Backbone,
        IndexRouter) {

        $(function() {
            var Router = new IndexRouter;
            Router.start();
        });

    }
);
