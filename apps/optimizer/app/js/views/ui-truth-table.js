function UITruthTable() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var table = null;
    var superHeaders = null;
    var headers = null;

    var container = null;

    ///////////// PUBLIC METHODS /////////////
    this.render = function() {
        var truthTableModel = pageViewController.truthTableViewController.truthTableModel;

        headers = truthTableModel.triggerLabels.concat(truthTableModel.actionLabels);

        var data = [];

        truthTableModel.rules.forEach(function(rule) {
            row = [];
            rule['triggers'].forEach(function(trigger) {
                var column = headers.indexOf(trigger['category']);
                var value = translateParams(trigger);
                row[column] = value;
            });
            var action = rule['action'];
            var actionColumn = headers.indexOf(action['category']);

            var value = translateParams(action);
            row[actionColumn] = value;
            data.push(row);
        });


        //TODO: d3 pattern?

        /************* Table Header *************/
        var header = table.append('thead');

        header.append('tr')
            .selectAll('th')
            .data(['Triggers', 'Actions']).enter()
            .append('th')
            .text(ƒ())
            .attr('colspan', function(d,i) {
                switch(i) {
                    case 0:
                        return truthTableModel.triggerLabels.length;
                    case 1:
                        return truthTableModel.actionLabels.length;
                }
            })
            .class("cell main-header")
            .classed("second-column-begin", function(d, i) {
                return i != 0;
            });

        header.append('tr')
            .selectAll('th')
            .data(headers).enter()
            .append('th')
            .class('cell')
            .class('sub-header')
            .text(function(d, i) {
                return d;
            })
            .classed("second-column-begin", function(d, i) {
                return i == truthTableModel.triggerLabels.length
            });

        /************* Table Body *************/
        table.append('tbody')
            .selectAll('tr')
            .data(data).enter()
            .append('tr')
            .each(function(d) {
                for(var i = 0; i < headers.length; i++) {
                    d3.select(this)
                        .append('td')
                        .class('cell')
                        .classed("second-column-begin", function() {
                            return i == truthTableModel.triggerLabels.length;
                        })
                        .classed("blank", function() {
                            return d[i] == undefined
                        })
                        .text(d[i])
                }
            })
    };

    this.renderBinary = function() {
        table.selectAll('*').remove();

        var truthTableModel = pageViewController.truthTableViewController.truthTableModel;

        var triggerHeaders = [];
        var triggerSuperHeaders = [];
        var actionHeaders = [];
        var actionSuperHeaders = [];

        var superHeaders = [];

        truthTableModel.triggerLabels.forEach(function(d) {
            triggerSuperHeaders = triggerSuperHeaders.concat({category: d['category'], span: d['values'].length});
            triggerHeaders = triggerHeaders.concat(d['values']);
        });

        truthTableModel.actionLabels.forEach(function(d) {
            actionSuperHeaders = actionSuperHeaders.concat({category: d['category'], span: d['values'].length});
            actionHeaders = actionHeaders.concat(d['values']);
        });

        headers = triggerHeaders.concat(actionHeaders);
        superHeaders = triggerSuperHeaders.concat(actionSuperHeaders);

        var headersDivider = 0;
        triggerSuperHeaders.forEach(function(t) {
            headersDivider += t['span'];
        });


        var data = [];

        truthTableModel.rules.forEach(function(rule) {
            row = [];
            rule['triggers'].forEach(function(trigger) {
                var column = headers.indexOf(trigger['category']);
                var value = translateParams(trigger);
                row[column] = value;
            });
            var action = rule['action'];
            var actionColumn = headers.indexOf(action['category']);

            var value = translateParams(action);
            row[actionColumn] = value;
            data.push(row);
        });


        //TODO: d3 pattern?

        /************* Table Header *************/
        var header = table.append('thead');

        header.append('tr')
            .selectAll('th')
            .data(['Triggers', 'Actions']).enter()
            .append('th')
            .text(ƒ())
            .attr('colspan', function(d,i) {
                switch(i) {
                    case 0:
                        return triggerHeaders.length;
                    case 1:
                        return actionHeaders.length;
                }
            })
            .class("cell main-header")
            .classed("second-column-begin", function(d, i) {
                return i != 0;
            });

        header.append('tr')
            .selectAll('th')
            .data(superHeaders).enter()
            .append('th')
            .text(ƒ('category'))
            .attr('colspan', ƒ('span'))
            .class("cell main-header")
            .classed("second-column-begin", function(d, i) {
                return i == triggerSuperHeaders.length;
            });

        header.append('tr')
            .selectAll('th')
            .data(headers).enter()
            .append('th')
            .class('cell')
            .class('sub-header')
            .text(function(d, i) {
                return d;
            })
            .classed("second-column-begin", function(d, i) {
                return i == headersDivider;
            });

        /************* Table Body *************/
        table.append('tbody')
            .selectAll('tr')
            .data(data).enter()
            .append('tr')
            .each(function(d) {
                var categories = [];
                for(var i = 0; i < headers.length; i++) {
                    d3.select(this)
                        .append('td')
                        .class('cell')
                        .classed("second-column-begin", function() {
                            return i == headersDivider;
                        })
                        .classed("blank", function() {
                            return d[i] == undefined
                        })
                        .text(function() {
                            if(d[i]) {
                                categories
                            }
                            return d[i]
                        })

                }
            })
    };


    ///////////// PRIVATE METHODS /////////////
    var translateParams = function(element) {
        console.log(element)
        return element['params'] != "" ? element['params'][0] + " - " + element['params'][1] : element['name']
    };


    var init = function() {
        container = d3.select('#content-main');

        table = container.selectAll('table')
            .data([""]);

        table.enter()
            .append('table')
            .attr('class','table table-hover table-striped table-bordered');

        table.selectAll('*').remove();

        var button = container.selectAll('button')
            .data(["Binarize", "Minimize"]);

        button.enter()
            .append('button')
            .text(ƒ())
            .class('btn btn-primary')
            .on('click', function(d,i) {
                switch(i) {
                    case 0:
                        pageViewController.truthTableViewController.getBinaryTable();
                }
            })


    }();
};