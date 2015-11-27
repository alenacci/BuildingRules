function TruthTableModel() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;

    var TRIGGERS = 0;
    var ACTIONS = 1;

    ///////////// PUBLIC VARIABLES //////////////
    self.headers = [];
    self.rows = [];

    self.headersIndexes = [];

    ///////////// PUBLIC METHODS //////////////
    this.setDataFromJSON = function(json) {
        console.log(json);

        var rules = json['rules'];

        // HEADERS
        rules.forEach(function(rule) {
            var triggers = rule['triggers'];
            var action = rule['action'];

            triggers.forEach(function(trigger) {
                var header = {};
                header.name = trigger['category'];
                header.description = trigger['categoryDescription'];
                appendHeaderIfNotExisting(header, TRIGGERS);
            });

            var actionHeader = {};
            actionHeader['name'] = action['category'];
            appendHeaderIfNotExisting(actionHeader, ACTIONS);

        });

        getHeaderIndex(self.headers);

        console.log(self.headers);
        console.log(self.getFirstActionIndex());

        // ROWS
        rules.forEach(function(rule) {
            var row = {};
            row.id = rule['id'];
            row.enabled = rule['enabled'];
            row.deleted = rule['deleted'];
            row.priority = rule['priority'];
            row.values = [];


            rule['triggers'].forEach(function(trigger) {
                var column = self.headersIndexes.indexOf(trigger['category']);
                var cell = {};
                cell.value = translateParams(trigger);
                cell.description = trigger['description'];

                row.values[column] = cell;

            });

            var action = rule['action'];
            var cell = {};
            var column = self.headersIndexes.lastIndexOf(action['category']);
            cell.value = translateParams(action);
            cell.description = action['description'];

            row.values[column] = cell;

            self.rows.push(row);
        });

        console.log(self.rows);

        pageViewController.truthTableViewController.drawTable();
    };

    this.setDataFromBinaryJSON = function(json) {
        // TODO:
        self.headers = json['labels'];


        self.rows = []

        pageViewController.truthTableViewController.drawTable();
    };

    this.getFirstActionIndex = function() {
        var current = self.headers[ACTIONS];
        while(current.children) {
            current = current.children
        }
        return self.headersIndexes.lastIndexOf(current[0].name);
    };

    ///////////// PRIVATE METHODS //////////////
    var appendHeaderIfNotExisting = function(header, section) {
        var headerList = self.headers[section].children;

        for(var i = 0; i < headerList.length; i++) {
            var h = headerList[i];
            if(h['name'] == header['name']) {
                return;
            }
        }
        headerList.push(header);
    };

    var getHeaderIndex = function(headers, indexes) {
        headers.forEach(function(h) {
            var current = h;
            if(current.children) {
                current = current.children;
                getHeaderIndex(current);
            }
            else {
                self.headersIndexes.push(current.name);
            }
        });
    };

    var translateParams = function(element) {
        var params =  element['translatedParams'];
        if(params && params[0] && params[1]) {
            return params[0] + " - " + params[1];
        }
        else if(params && params[0]) {
            return params[0];
        }
        else {
            return element['name'];
        }
    };


    var init = function() {
        self.headers = [
            {
                'name': 'Triggers',
                'description': '',
                'children': []
            },
            {
                'name': 'Actions',
                'description': '',
                'children': []
            }
        ]
    }();
}