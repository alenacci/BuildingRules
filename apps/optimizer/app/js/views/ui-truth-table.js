function UITruthTable() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var table = null;
    var headers = null;
    var rows = null;

    var container = null;

    ///////////// PUBLIC METHODS /////////////
    this.render = function() {
        table.selectAll('*').remove();

        var truthTableModel = pageViewController.truthTableViewController.truthTableModel;
        headers = truthTableModel.headers;
        rows = truthTableModel.rows;

        /************* Table Header *************/
        var header = table.append('thead');

        //var headerRow = headers;
        var headerRow = clone(headers);
        var level = 0;
        var firstActionIndex = 2;

        for(; headerRow.length != 0; level++) {
            var newSpan = 0;

            //console.log(headerRow);

            headerRow.unshift({'name':'ID'});
            headerRow.push({'name':'Priority'});

            header.append('tr')
                .selectAll('th')
                .data(headerRow).enter()
                .append('th')
                .text(function(d,i){
                    if(i != 0 && i != headerRow.length-1 || level == 0) {
                        return d['name'];
                    }
                })
                .attr('colspan', function(d) {
                    return getTotalChildren(d);
                })
                .class('cell')
                .classed('main-header', function() {
                    return level == 0;
                })
                .each(function(d,i){
                    if(i < firstActionIndex) {
                        var span = (d.children === undefined) ? 1 : d.children.length;
                        newSpan += span;
                    }
                })
                .classed('second-column-begin', function(d,i) {
                    return i == firstActionIndex;
                })
                .attr('title', ƒ('description'))
                .classed('id', function(d,i) {
                    return i == 0;
                })
                .classed('priority', function(d,i) {
                    return i == headerRow.length-1;
                });


            // Build the new level of headers
            hR = [];
            headerRow.forEach(function(h) {
                if(h.children) {
                    hR = hR.concat(h.children);
                }
            });
            headerRow = hR;
            firstActionIndex = newSpan;
        }

        /************* Table Body *************/
        table.append('tbody')
            .selectAll('tr')
            .data(rows).enter()
            .append('tr')
            .classed('deleted', ƒ('deleted'))
            .classed('disabled', function(d){
                return !d.enabled;
            })
            .each(function(d) {
                var cells = d['values'];

                cells[truthTableModel.headersIndexes.length] = ({'value': d['priority']});
                cells.unshift({'value': d['id']});

                for(var i = 0; i < cells.length; i++) {
                    d3.select(this)
                        .append('td')
                        .class('cell')
                        .classed("second-column-begin", function() {
                            return i == truthTableModel.getFirstActionIndex() + 1;
                        })
                        .classed("blank", function() {
                            return cells[i] == undefined
                        })
                        .text(function(){
                            if(cells[i]) {
                                return cells[i].value;
                            }
                        })
                        .attr('title', function(){
                            if(cells[i]) {
                                return cells[i].description;
                            }
                        })
                        .classed('id', function() {
                            return i == 0;
                        })
                        .classed('priority', function() {
                            return i == cells.length-1;
                        });
                }
            })
    };

    self.fillHeader = function(building, room, rules) {
        var header = d3.select('#content-main')
            .select('h1')
            .text(function() {
                return building + " " + room;
            });

        if(rules) {
            header.append('small')
                .text(' - ' + rules + " rules")
        }
    };

    //////////// PRIVATE METHODS /////////////
    var getTotalChildren = function(header, total) {
        var total = total | 0;

        var children = header.children;

        if(children) {
            for(var i = 0; i < children.length; i++) {
                var child = children[i];
                total = getTotalChildren(child, total);
            }
        }
        else {
            total += 1;
        }
        return total;

    };

    var init = function() {
        container = d3.select('#content-main');

        table = container.selectAll('table')
            .data([""]);

        table.enter()
            .append('table')
            .attr('class','table table-hover table-striped table-bordered');

        table.selectAll('*').remove();

        var button = container.select('#buttons')
            .selectAll('button')
            .data(["Binarize", "Minimize"]);

        button.enter()
            .append('button')
            .text(ƒ())
            .class('btn btn-primary')
            .on('click', function(d,i) {
                switch(i) {
                    case 0:
                        pageViewController.truthTableViewController.getBinaryTable();
                        break;
                    case 1:
                        pageViewController.truthTableViewController.getMinimizedTable();
                        break;
                }
            })


    }();
};