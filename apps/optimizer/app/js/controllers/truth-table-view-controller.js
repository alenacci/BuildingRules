function TruthTableViewController(building, room) {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var building = building;
    var room = room;
    var truthTableView = null;

    ///////////// PUBLIC VARIABLES /////////////
    this.truthTableModel = null;

    ///////////// PUBLIC METHODS /////////////
    this.drawTable = function(binary) {
        truthTableView.render();
    };

    this.getBinaryTable = function() {
        var query = "api/rule_optimizer/binary_truth_table/" + building + "/" + room;

        getQuery(query, function(json) {
            self.truthTableModel.setDataFromBinaryJSON(json);
        });
    };

    ///////////// PRIVATE METHODS ////////////
    var retrieveData = function() {
        var query = "api/rule_optimizer/truth_table/" + building + "/" + room;

        getQuery(query, function(json) {
            self.truthTableModel.setDataFromJSON(json);
        });
    };

    var init = function() {
        self.truthTableModel = new TruthTableModel(self);
        truthTableView = new UITruthTable(self);
        retrieveData();
    }();

}