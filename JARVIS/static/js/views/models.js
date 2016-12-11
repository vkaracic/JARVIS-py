define([
        'jquery',
        'underscore',
        'underscore.string',
        'backbone',
        'text!js/templates/models.html',
        'datatables'
    ], function($,
                _,
                _s,
                Backbone,
                ModelsTemplate) {

        return Backbone.View.extend({
            template: _.template(ModelsTemplate),

            updateTable: function() {
                var data = this.collection.map(this.getModelData, this),
                    $table = this.$('#models-table').DataTable();
                $table.clear().rows.add(data).draw();
                return this;
            },

            initialize: function() {
                $('.queue-link').removeClass('active');
                $('.models-link').addClass('active');
                $('.team-link').removeClass('active');
                this.listenTo(this.collection, 'update', this.updateTable);
            },

            renderModelsTable: function() {
                if (!$.fn.dataTable.isDataTable('#models-table')) {
                    this.$('#models-table').DataTable({
                        bLengthChange: false,
                        language: {
                            searchPlaceholder: 'Search',
                            sSearch: ''
                        },
                        columns: [
                            {
                                title: 'ID',
                                data: 'id',
                            },
                            {
                                title: 'Title',
                                data: 'title',
                            },
                            {
                                title: 'Hash',
                                data: 'hash',
                                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                                    $(nTd).html('<a href="/#models/'+oData.id+'">'+oData.hash+'</a>');
                                }
                            },
                            {
                                title: 'Structure',
                                data: 'structure'
                            },
                            {
                                title: 'Cost',
                                data: 'cost'
                            },
                            {
                                title: 'Optimizer',
                                data: 'optimizer'
                            },
                            {
                                title: 'Activation',
                                data: 'activation'
                            },
                            {
                                title: 'Trained',
                                data: 'trained'
                            },
                            {
                               title: 'Latest cost',
                               data: 'latest_cost' 
                            }
                        ]
                    });
                }
            },

            getModelData: function(model) {
                var structure = _s.sprintf(
                    '%s-%s-%s', model.get('num_inputs'), model.get('num_hidden'), model.get('num_outputs')
                );
                return {
                    id: model.get('id'),
                    title: model.get('title'),
                    hash: model.get('external_id'),
                    structure: structure,
                    cost: model.get('cost'),
                    optimizer: model.get('optimizer'),
                    activation: model.get('activation'),
                    trained: model.get('trained'),
                    latest_cost: model.get('latest_cost'),
                };
            },

            render: function() {
                this.collection.fetch();
                this.$el.html(this.template(this.collection));
                this.renderModelsTable();
                this.updateTable();
                return this;
            }
        });
    }
);