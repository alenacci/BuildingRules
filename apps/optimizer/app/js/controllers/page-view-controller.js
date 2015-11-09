function PageViewController() {
    ///////////// PRIVATE VARIABLES /////////////
    var self = this;
    var sessionParams;
    var model;

    ///////////// PUBLIC VARIABLES //////////////
    this.truthTableViewController = null;


    ///////////// PUBLIC METHODS /////////////
    this.truthTable = function(building, room) {
        this.truthTableViewController = new TruthTableViewController(building, room);
    };

    this.drawSidebar = function() {
        var buildings = model.buildings;

        d3.select('#sidebar')
            .selectAll('ul')
            .data(buildings).enter()
            .append('ul')
            .class('nav nav-sidebar')
            .text(ƒ('name'))
            .selectAll('li')
            .data(ƒ('rooms')).enter()
            .append('li')
            .append('a')
            .attr('href', "")
            .text(ƒ('roomName'))
    };

    ///////////// PRIVATE METHODS /////////////
    var retrieveBuildingsAndRooms = this.retrieve = function() {
            postQuery("api/users/admin/buildings", function(json) {
                var buildings = json['buildings'];

                model = new Model();

                buildings.forEach(function(b) {
                    var buildingName = b['buildingName'];
                    postQuery("api/users/admin/buildings/" + buildingName + "/rooms", function(json){

                        var buildingRooms = {
                            name: buildingName,
                            rooms: json['rooms']
                        };
                        model.buildings.push(buildingRooms);
                        self.drawSidebar();
                    }, sessionParams);
                });



            }, sessionParams)
    };

    var login = function(callback) {
        var query = "api/users/admin/login";
        var params = [
            {key: "password",
                value:"brulesAdmin2014"
            }
        ];
        postQuery(query, function(json) {
            sessionParams = [
                {key: "userUuid", value: json['userUuid']},
                {key: "sessionKey", value: json['sessionKey']},
            ];

            callback();
        }, params);
    };

    var init = function() {
        login(retrieveBuildingsAndRooms);
    }();

};
