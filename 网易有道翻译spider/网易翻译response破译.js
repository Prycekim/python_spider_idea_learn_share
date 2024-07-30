const aescrypto = require('crypto');
const crypto = require('crypto');
const args = process.argv.slice(2);
const e = args[0];



function T(e) {
    return crypto.createHash("md5").update(e).digest()
}

function aes(e){
    const a = Buffer.alloc(16, T(t))
      , n = Buffer.alloc(16, T(o))
      , r = aescrypto.createDecipheriv("aes-128-cbc", a, n);
    let l = r.update(e, "base64", "utf-8");
    return l += r.final("utf-8"),
    l
}
// new Uint8Array([8, 20, 157, 167, 60, 89, 206, 98, 85, 91, 1, 233, 47, 52, 232, 56])
// new Uint8Array([210, 187, 27, 253, 232, 59, 56, 195, 68, 54, 99, 87, 183, 156, 174, 28])

const t = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"

const o = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"





console.log(ss = aes(e))