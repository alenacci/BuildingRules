var sessionParams = undefined;

/***
 * Query the API after being logged and having created a session.
 * @param query
 * @param fun
 */
apiQuery = function(query, fun) {
    var executeQuery = function() {
        postQuery(query, fun, sessionParams);
    };

    if(!sessionParams) {
        login(executeQuery)
    }
    else {
        executeQuery();
    }
};

/***
 * Login API query
 * @param callback
 */
login = function(callback) {
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

/***
 * GET HTTP request
 * @param query
 * @param fun
 */
getQuery = function(query, fun) {
    d3.json("http://localhost:5003/" + query, function(error, json) {
        if (error) return;
        if (!json["request-success"] || json["request-error"]) return;
        fun(json)
    });
};

/***
 * POST HTTP request
 * @param query
 * @param fun
 * @param postParams
 */
postQuery = function(query, fun, postParams) {
    //d3.json("http://localhost:5003/" + query, function(error, json) {
    //
    //    fun(json)
    //}).header("Content-Type","multipart/form-data")
    //    .send("POST",postParams || "");

    //$.post(, postParams, fun);

    var fd = false;

    if(postParams instanceof Array) {
        fd = new FormData();
        postParams.forEach(function (param) {
            fd.append(param['key'], param['value']);
        });
    }

    $.ajax({
        url: "http://localhost:5003/" + query,
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            if (!data["request-success"] || data["request-error"]) return;
            fun(data);
        }
    });

};