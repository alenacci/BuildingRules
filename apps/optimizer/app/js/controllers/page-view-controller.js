function PageViewController() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;

    ///////////// PUBLIC VARIABLES //////////////
    this.truthTableViewController = null;


    ///////////// PUBLIC METHODS /////////////
    this.truthTable = function(building, room) {
        this.truthTableViewController = new TruthTableViewController(building, room);
    };

    var init = function() {
    }();

};
