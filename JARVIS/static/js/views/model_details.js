define([
        'underscore',
        'backbone',
        'js/models/model',
        'text!js/templates/model_details.html'

    ], function(_,
                Backbone,
                ModelModel,
                ModelDetailsTemplate) {

    return Backbone.View.extend({
        template: _.template(ModelDetailsTemplate),

        initialize: function(options) {
            var self = this;
            this.id = options.id;
            this.model = ModelModel.findOrCreate({id: this.id});
            this.model.fetch().done(function() {
                self.render();
            });
        },

        drawTrainingResults: function(hash) {
            var self = this;
            $.ajax({
                url: '/api/results/' + hash + '/',
                success: function(data) {
                    var results = [];
                    var tmp = data.results.split(',');
                    _.each(tmp, function(item, i) {
                        results.push({
                            y: parseFloat(item),
                            x: i
                        });
                    });
                    self.drawGraph(results);
                }
            });
        },

        drawGraph: function(results) {
            var ctx = $("#training-results");
            var myChart = new Chart(ctx, {
                type: 'line',
                    data: {
                        datasets: [{
                            label: 'Error Rate',
                            data: results
                        }]
                    },
                    options: {
                        maintainAspectRatio: false,
                        responsive:false,
                        scales: {
                            xAxes: [{
                                type: 'linear',
                                position: 'bottom'
                            }]
                        }
                    }
            });
        },

        render: function() {
            console.log(this.model.attributes);
            this.$el.html(this.template(this.model.attributes));
            this.drawTrainingResults(this.model.get('external_id'));
        }
    });
});
