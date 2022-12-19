const execSync = require('child_process').execSync;
const path = require('path');
const fs = require('fs');

function run(cmd){
    console.log("----- Run -----")
    console.log("Command:",cmd)
    let output = execSync(cmd, { encoding: 'utf-8' });
    console.log('Output was:\n', output);
    console.log("----- End -----")
}

// Paths
const alteryx_path     = 'C:\\Program Files\\Alteryx\\bin\\AlteryxEngineCmd.exe'
const source_path      = path.join(__dirname,"alteryx_src","Supporting_Macros")
const dest_path        = path.join(__dirname,"PDFWatermark","PDFWatermark","Supporting_Macros") 
 
var cmds   = []
var macros = fs.readdirSync(source_path).filter(Element=>{ return path.extname(Element)== ".yxmc" })
var macro_other_files =  fs.readdirSync(source_path).filter(Element=>{ return path.extname(Element)== ".png" })

console.log("Macros:",macros)
console.log("macro_other_files:",macro_other_files)
if (process.env.NODE_ENV == 'production'){
    //Pack Macro
    macros.forEach(element=>{
        let cmd = ` "${alteryx_path}"  /Lock "${source_path}\\${element}" "${dest_path}\\${element}"`
        cmds.push(cmd)
    })
    macro_other_files.forEach(element=>{
        let cmd = ` copy "${source_path}\\${element}" "${dest_path}\\${element}"`
        cmds.push(cmd)
    })
} else {
    //Pack Macro
    macros.forEach(element=>{
        let cmd = ` copy "${source_path}\\${element}" "${dest_path}\\${element}"`
        cmds.push(cmd)
    })
}

cmds.forEach(element => { run(element) })