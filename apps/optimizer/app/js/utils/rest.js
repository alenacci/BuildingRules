getQuery = function(query, fun) {
    d3.json("http://localhost:5003/" + query, function(error, json) {
        if (error) return;
        if (!json["request-success"] || json["request-error"]) return;
        fun(json)
    });
};

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