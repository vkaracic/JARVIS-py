define([
        'underscore',
        'backbone',
        'js/models/model',
        'text!js/templates/model_details.html',
        'js-cookie'
    ], function(_,
                Backbone,
                ModelModel,
                ModelDetailsTemplate,
                Cookie) {

    return Backbone.View.extend({
        template: _.template(ModelDetailsTemplate),

        events: {
            'click .run-inference': 'runInference'
        },

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
                    if (!_.isEmpty(data)) {
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
                    },
                }
            });
        },

        updateInferenceResults: function(input, output) {
            var table = $('.inference-results');
            table.find('tr').remove();
            for (var i = 0; i < output.length; i++) {
                table.append(
                    '<tr>'+
                    '<td>'+input.input_data[i]+'</td>'+
                    '<td>'+output[i]+'</td>'+
                    '</tr>'
                );
            }
            return this;
        },

        submitInference: function(data) {
            var self = this;
            $.ajax({
                url: '/api/private/models/' + this.model.id +'/',
                method: 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': Cookie.get('csrftoken')
                },
                data: JSON.stringify(data),
                success: function(res) {
                    console.log("SUCCESS!");
                    self.updateInferenceResults(data, res);
                },
                error: function() {
                    console.log('ERROR');
                }
            });
        },

        runInference: function(e) {
            e.preventDefault();

            var raw_data = this.$('.form-input textarea').val(),
                input_data = [];

            _.each(raw_data.split('\n'), function(item) {
                input_data.push(item.split(',').map(function(i) {
                    return parseFloat(i);
                }));
            });
            this.submitInference({
                input_data: input_data
            });
        },

        render: function() {
            this.$el.html(this.template(this.model.attributes));
            if (this.model.get('permission_type') === 0) {
                $('.permission-type').text('Free use');
            } else if (this.model.get('permission_type') === 1) {
                $('.permission-type').text('Only me');
            } else {
                $('.permission-type').text('Only my team');
            }
            this.drawTrainingResults(this.model.get('external_id'));
        }
    });
});
