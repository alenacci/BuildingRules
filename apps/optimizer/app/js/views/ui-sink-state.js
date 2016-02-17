function UISinkState() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var container = null;
    var table = null;

    ///////////// PUBLIC METHODS /////////////
    this.render = function() {
        container.selectAll('#rules').remove();

        container.select('#buttons')
            .selectAll('button').remove()

        table = container.append('div').attr('id','rules');

        var data = pageViewController.sinkStateViewController.sinkStateModel.data;
        console.log(data)

        var rules = data.rules;
        var assertiveRules = data.assertiveRules;
        var uselessRules = data.uselessRules;
        var sinks = data.sinks;
        var semiSinks = data.semiSinks;

        console.log(rules);

        table.append('h3').text('Rules');
        if(Object.keys(rules).length > 0) {
            for (r in rules) {
                paragraph = table.append('p')
                paragraph.append('b').text(r)
                paragraph.append('i').text(' - ' + rules[r])
            }
        }
        else
        {
            table.append('h5').text('No rules')
        }



        table.append('h3').text('Assertive Rules');
        if(Object.keys(assertiveRules).length > 0) {
            for (r in assertiveRules) {
                rule = assertiveRules[r];
                paragraph = table.append('p')
                paragraph.append('b').text(r)
                paragraph.append('i').text(' - ' + rule.description)
                paragraph.append('b').text(' - influence: ' + rule.influence)
            }
        }else {
            table.append('h5').text('No rules')
        }

        table.append('h3').text('Useless Rules');
        if(Object.keys(uselessRules).length > 0) {
            for (r in uselessRules) {
                rule = assertiveRules[r];
                paragraph = table.append('p')
                paragraph.append('b').text(r)
                paragraph.append('i').text(' - ' + rule.description)
                paragraph.append('b').text(' - influence: ' + rule.influence)
            }
        }else {
            table.append('h5').text('No rules')
        }

        table.append('h3').text('Sinks');
        if(Object.keys(sinks).length > 0) {
            for (r in sinks) {
                rule = sinks[r];
                paragraph = table.append('p')
                paragraph.append('b').text(r)
                paragraph.append('i').text(' - ' + rule.description)
                paragraph.append('b').text(' - influence: ' + rule.influence)
                list = table.append('ul')
                list.append('li').text('No opposite rules defined!')

            }
        }else {
            table.append('h5').text('No rules')
        }

        table.append('h3').text('Semi Sinks');
        if(Object.keys(semiSinks).length > 0) {
            for (r in semiSinks) {
                rule = semiSinks[r];
                paragraph = table.append('p')
                paragraph.append('b').text(r)
                paragraph.append('i').text(' - ' + rule.description)
                paragraph.append('b').text(' - influence: ' + rule.influence)
                list = table.append('ul');
                for(var i = 0; i < rule.opposites.length; i++) {
                    o = rule.opposites[i];
                    console.log(o)
                    p = list.append('li')
                    paragraph = p.append('p')
                    paragraph.append('b').text(o.id)
                    paragraph.append('i').text(' - ' + o.description)
                    paragraph.append('b').text(' - influence: ' + o.influence)

                }
            }

        }else {
            table.append('h5').text('No rules')
        }



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

    var init = function() {
        container = d3.select('#content-main');

        container.selectAll('table').selectAll('*').remove();

    }();
};