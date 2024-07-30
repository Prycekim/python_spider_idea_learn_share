const crypto = require('crypto');

const time = (new Date).getTime();




function _(e) {
    return crypto.createHash("md5").update(e.toString()).digest("hex")
}

function S(time, t) {
    const u = "fanyideskweb"
    const d = "webfanyi"
    return _(`client=${u}&mysticTime=${time}&product=${d}&key=${t}`)
}


function k(time) { 
    const t = "fsdsogkndfokasodnaso"
    return [S(time,t),time]

}


console.log(k(time))
// console.log('sign是：')
// console.log(res['sign'])
// console.log('mysticTime是：')
// console.log(res['mysticTime'])
