function PageViewController() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    this.model = undefined;

    ///////////// PUBLIC VARIABLES //////////////
    self.truthTableViewController = null;
    self.building = undefined;
    self.room = undefined;


    ///////////// PUBLIC METHODS /////////////
    this.truthTable = function() {
        this.truthTableViewController = new TruthTableViewController(self.building, self.room);
    };

    this.drawSidebar = function() {
        var buildings = self.model.buildings;

        // SELECT
        var buildingLabels = d3.select('#sidebar')
            .selectAll('ul')
            .data(buildings);

        // ENTER
        buildingLabels
            .enter()
            .append('ul')
            .class('nav nav-sidebar')
            .text(ƒ('name'));

        // EXIT
        buildingLabels.exit().remove();


        buildingLabels.each(function() {

            // SELECT
            var roomLabels = d3.select(this)
                .selectAll('li')
                .data(ƒ('rooms'));

            // ENTER
            roomLabels.enter()
                .append('li')
                .append('a')
                .attr('href', "#")
                .text(ƒ('roomName'))
                .on("click", function(d) {
                    self.building = d['buildingName'];
                    self.room = d['roomName'];
                    self.truthTable();
                    self.drawSidebar();
                });

            // UPDATE
            roomLabels.classed("active", function(d) {
                return self.building == d['buildingName'] && self.room == d['roomName'];
            });

            // EXIT
            roomLabels.exit().remove();
        });

    };

    ///////////// PRIVATE METHODS /////////////
    var retrieveBuildingsAndRooms = this.retrieve = function() {
            apiQuery("api/users/admin/buildings", function(json) {
                var buildings = json['buildings'];

                self.model = new Model();

                buildings.forEach(function(b) {
                    var buildingName = b['buildingName'];
                    apiQuery("api/users/admin/buildings/" + buildingName + "/rooms", function(json){

                        var buildingRooms = {
                            name: buildingName,
                            rooms: json['rooms']
                        };
                        self.model.buildings.push(buildingRooms);
                        self.drawSidebar();
                    });
                });
            });
    };


    var init = function() {
        retrieveBuildingsAndRooms();
    }();

};
