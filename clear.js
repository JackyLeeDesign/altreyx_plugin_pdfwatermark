const fs = require('fs');
const path = require('path');

const dir       = path.join(__dirname,"PDFWatermark")
const to_delete = fs.readdirSync(dir).filter(item => item !== "Config.xml")

console.log("Item to Delete...",to_delete)

to_delete.forEach((item)=>{
    let target = path.join(dir,item)
    fs.rmSync(target,{ recursive: true, force: true })
    console.log(target,"deleted.")
})



