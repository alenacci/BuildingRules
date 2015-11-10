function UITruthTable() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var table = null;
    var headers = null;

    var container = null;

    ///////////// PUBLIC METHODS /////////////
    this.render = function() {
        console.log("UITruthTable.render()");
        var truthTableModel = pageViewController.truthTableViewController.truthTableModel;

        headers = truthTableModel.triggerLabels.concat(truthTableModel.actionLabels);

        var data = [];

        truthTableModel.rules.forEach(function(rule) {
            row = [];
            rule['triggers'].forEach(function(trigger) {
                var column = headers.indexOf(trigger['category']);
                var params = translateParams(trigger['params']);
                row[column] = params;
            });
            var action = rule['action'];
            var actionColumn = headers.indexOf(action['category']);

            var params = translateParams(action['params']);
            row[actionColumn] = params;
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


    ///////////// PRIVATE METHODS /////////////
    var translateParams = function(params) {
        // Handle the case in which ranges are defined. NB range can be defined only with two values.
        if(params instanceof Object) {
            params = params[0] + " - " + params[1]
        }
        return params;
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


    }();
};