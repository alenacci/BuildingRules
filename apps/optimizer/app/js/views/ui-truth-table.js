function UITruthTable() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var table = null;
    var headers = null;

    ///////////// PUBLIC METHODS /////////////
    this.render = function() {
        console.log("UITruthTable.render()");
        var truthTableModel = pageViewController.truthTableViewController.truthTableModel;

        headers = truthTableModel.triggerLabels.concat(truthTableModel.actionLabels);
        var secondColumnBegin = truthTableModel.triggerLabels.length;

        var columns = [], data = [];

        headers.forEach(function(h, i) {
            columns.push({
                field: 'field' + i,
                title: h
            })
        });

        truthTableModel.rules.forEach(function(rule) {
            row = {};
            rule['triggers'].forEach(function(trigger) {
                var column = headers.indexOf(trigger['category']);
                var params = translateParams(trigger['params']);
                row['field'+column] = params;
            });
            var action = rule['action'];
            var actionColumn = headers.indexOf(action['category']);

            var params = translateParams(action['params']);
            row['field'+actionColumn] = params;
            data.push(row);
        });

        //// Table Header
        //table.append('thead').append('tr')
        //    .selectAll('th')
        //    .data(headers).enter()
        //    .append('th')
        //    .classed('data-field', true)
        //    .text(function(d, i) {
        //        return d;
        //    })
        //    .classed("second-column-begin", function(d, i) {
        //        if(i == secondColumnBegin) {
        //            return true;
        //        }
        //        return false;
        //    });
        //
        //// Table body
        //table.append('tbody')
        //    .selectAll('tr')
        //    .data(data).enter()
        //    .append('tr')
        //    .selectAll('td')
        //    .data(function(d, i) {
        //        console.log(d);
        //        return d;
        //    })
        //    .enter()
        //    .append('td')
        //    .text(function(d,i) {
        //        console.log(d);
        //    })



        table = $('table');
        table.bootstrapTable('destroy').bootstrapTable({
            columns: columns,
            data: data
        });


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
        table = d3.select('body')
            .append('table')
            .attr('class','table table-hover')
    }();
};