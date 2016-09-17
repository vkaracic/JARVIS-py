define([
        'jquery',
        'underscore',
        'backbone',
        'text!js/templates/queue.html',
        'datatables'
    ], function($,
                _,
                Backbone,
                QueueTemplate) {

        return Backbone.View.extend({
            template: _.template(QueueTemplate),

            updateTable: function() {
                var data = this.collection.map(this.getTaskData, this),
                    $table = this.$('#task-table').DataTable();
                $table.clear().rows.add(data).draw();
                return this;
            },

            initialize: function() {
                this.listenTo(this.collection, 'update', this.updateTable);
            },

            renderTaskTable: function() {
                if (!$.fn.dataTable.isDataTable('#task-table')) {
                    this.$('#task-table').DataTable({
                        columns: [
                            {
                                title: 'ID',
                                data: 'id',
                            },
                            {
                                title: 'Model',
                                data: 'model'
                            },
                            {
                                title: 'Priority',
                                data: 'priority'
                            },
                            {
                                title: 'Started At',
                                data: 'started_at'
                            },
                            {
                                title: 'Status',
                                data: 'status'
                            }
                        ]
                    });
                }
            },

            getTaskData: function(task) {
                return {
                    id: task.get('id'),
                    model: task.get('model'),
                    priority: task.get('priority'),
                    started_at: task.get('started_at'),
                    status: task.get('status'),
                };
            },

            render: function() {
                this.collection.fetch();
                this.$el.html(this.template(this.collection));
                this.renderTaskTable();
                this.updateTable();
                return this;
            }
        });
    }
);