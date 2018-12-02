// signature: r.getHMAC("HEX")

function r(e, t) {
    var n = Date.now(),
        r = new i.a("SHA-1", "TEXT");
    return r.setHMACKey("d1b964811afb40118a12068ff74a12f4", "TEXT"), r.update(e), r.update(s), r.update("com.zhihu.web"),
        r.update(String(n)),
        u({
            clientId: s,
            grantType: e,
            timestamp: n,
            source: "com.zhihu.web",
            signature: r.getHMAC("HEX")
        }, t)
}

this.getHMAC = function (t, n) {
    var r, i, v, y;
    if (!1 === w) throw Error("Cannot call getHMAC without first setting HMAC key");
    switch (v = m(n), t) {
        case "HEX":
            r = function (e) {
                return f(e, a, v)
            };
            break;
        case "B64":
            r = function (e) {
                return p(e, a, v)
            };
            break;
        case "BYTES":
            r = function (e) {
                return d(e, a)
            };
            break;
        case "ARRAYBUFFER":
            try {
                r = new ArrayBuffer(0)
            } catch (e) {
                throw Error("ARRAYBUFFER not supported by this environment")
            }
            r = function (e) {
                return h(e, a)
            };
            break;
        default:
            throw Error("outputFormat must be HEX, B64, BYTES, or ARRAYBUFFER")
    }
    return i = u(g.slice(), E, b, l(o), a), y = s(O, B(e)), y = u(i, a, c, y, a), r(y)
}

function m(e) {
    var t = {
        outputUpper: !1,
        b64Pad: "=",
        shakeLen: -1
    };
    if (e = e || {}, t.outputUpper = e.outputUpper || !1, !0 === e.hasOwnProperty("b64Pad") && (t.b64Pad = e.b64Pad), !0 === e.hasOwnProperty("shakeLen")) {
        if (0 != e.shakeLen % 8) throw Error("shakeLen must be a multiple of 8");
        t.shakeLen = e.shakeLen
    }
    if ("boolean" != typeof t.outputUpper) throw Error("Invalid outputUpper formatting option");
    if ("string" != typeof t.b64Pad) throw Error("Invalid b64Pad formatting option");
    return t
}


function f(e, t, n) {
    var r = "";
    t /= 8;
    var o, i;
    for (o = 0; o < t; o += 1) i = e[o >>> 2] >>> 8 * (3 - o % 4), r += "0123456789abcdef".charAt(i >>> 4 & 15) + "0123456789abcdef".charAt(15 & i);
    return n.outputUpper ? r.toUpperCase() : r
}