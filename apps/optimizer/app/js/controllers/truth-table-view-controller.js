function TruthTableViewController(building, room) {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var building = building;
    var room = room;
    var truthTableView = null;

    ///////////// PUBLIC VARIABLES /////////////
    this.truthTableModel = null;

    ///////////// PUBLIC METHODS /////////////
    this.drawTable = function() {
        truthTableView.render();
    };

    ///////////// PRIVATE METHODS ////////////
    var retrieveData = function() {
        var query = "http://localhost:5003/api/rule_optimizer/truth_table/" + building + "/" + room;

        d3.json(query, function (error, json) {
            if (error) return;
            if (!json["request-success"] || json["request-error"]) return;
            self.truthTableModel.setDataFromJSON(json);
        });
    };


    var init = function() {
        self.truthTableModel = new TruthTableModel(self);
        truthTableView = new UITruthTable(self);
        retrieveData();
    }();

}