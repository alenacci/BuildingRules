function SinkStateViewController(building, room) {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var building = building;
    var room = room;
    var sinkStateView = null;

    ///////////// PUBLIC VARIABLES /////////////
    this.sinkStateModel = null;

    ///////////// PUBLIC METHODS /////////////
    this.drawResults = function() {
        sinkStateView.fillHeader(building, room);
        sinkStateView.render();
    };


    ///////////// PRIVATE METHODS ////////////
    var retrieveData = function() {
        var query = "api/sink_state_analysis/" + building + "/" + room;

        getQuery(query, function(json) {
            self.sinkStateModel.setDataFromJSON(json);
        });
    };

    var init = function() {
        self.sinkStateModel = new SinkStateModel(self);
        sinkStateView = new UISinkState(self);
        retrieveData();
    }();

}