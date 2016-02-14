function SinkStateModel() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;

    ///////////// PUBLIC VARIABLES //////////////
    self.data = [];


    ///////////// PUBLIC METHODS //////////////
    this.setDataFromJSON = function(json) {
        self.data['rules'] = json['rules'];
        self.data['assertiveRules'] = json['assertive_rules'];
        self.data['uselessRules'] = json['useless_rules'];
        self.data['sinks'] = json['sinks'];
        self.data['semiSinks'] = json['semi_sinks'];

        pageViewController.sinkStateViewController.drawResults();
    };
    var init = function() {
    }();
}