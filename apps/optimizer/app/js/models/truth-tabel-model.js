function TruthTableModel() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;

    ///////////// PUBLIC VARIABLES //////////////
    self.triggerLabels = [];
    self.actionLabels = [];
    self.rules = [];

    ///////////// PUBLIC METHODS //////////////
    this.setDataFromJSON = function(json) {
        console.log(json);

        self.triggerLabels = json['triggerLabels'];
        self.actionLabels = json['actionLabels'];
        self.rules = json['rules'];

        pageViewController.truthTableViewController.drawTable();
    };

    var init = function() {
    }();
}