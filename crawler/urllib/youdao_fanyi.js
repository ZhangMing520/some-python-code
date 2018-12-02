var r = function (e) {
    var t = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10));
    return {
        salt: t,
        sign: n.md5("fanyideskweb" + e + t + "sr_3(QOHT)L2dx#uuGR@r")
    }
};

var x = f("#inputOriginal");
var T = f(".fonts__over");

var n = x.val(),
    r = g.generateSaltSign(n),
    i = n.length;
if (F(), T.text(i), i > 5e3) {
    var a = n;
    n = a.substr(0, 5e3), r = g.generateSaltSign(n);
    var s = a.substr(5e3);
    s = (s = s.trim()).substr(0, 3),
        f("#inputTargetError").text("有道翻译字数限制为5000字，“" + s + "”及其后面没有被翻译!").show(),
        T.addClass("fonts__overed")
} else {
    T.removeClass("fonts__overed"), f("#inputTargetError").hide();
}