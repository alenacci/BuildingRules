function TruthTableModel() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;

    ///////////// PUBLIC VARIABLES //////////////
    self.triggerLabels = [];
    self.actionLabels = [];
    self.rules = [];
    self.binary = undefined;

    ///////////// PUBLIC METHODS //////////////
    this.setDataFromJSON = function(json) {
        console.log(json);

        self.triggerLabels = json['triggerLabels'];
        self.actionLabels = json['actionLabels'];
        self.rules = json['rules'];
        self.binary = json['binary'];

        pageViewController.truthTableViewController.drawTable(self.binary);
    };

    var init = function() {
    }();
}