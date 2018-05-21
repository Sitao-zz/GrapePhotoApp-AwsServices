module.exports = {
    getResultSingle: function (obj) {
        var array=[];
        array.push(obj)
        var result = {
            "success":true,
            "result":array,
            "error":null
        };
        return result;
    },
    getResultMultiple: function (obj) {
        var result = {
            "success":true,
            "result":obj,
            "error":null
        };
        return result;
    },
    getReultError: function (msg) {
        var result = {
          "success":false,
          "result":null,
          "error":msg
        };
        return result;
    }
};
