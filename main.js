// debugger
const { VM, VMScript } = require("vm2")
const fs = require("fs");

const path = require("path");
const cheerio = require('cheerio')
// const bodomparse = require('xmldom').DOMParser
const {createCanvas}=require('canvas')
// const CryptoJS = require("crypto-js");  // npm install crypto-js

let run_path= path.resolve(__dirname, './run/');
let config_path = path.resolve(__dirname, './config/');
let tools_path=path.resolve(__dirname, './tools/');
const tools=require(`${config_path}/tools.config`)
const env=require(`${config_path}/env.config`)

//名称
// 清空;
// console.log(run_path);
fs.writeFileSync(`${run_path}/log.txt`,"")
// fs.writeFileSync(__dirname + '/run/log.txt',"")

let bohtml_=fs.readFileSync(`${run_path}\\run.html`).toString('utf-8')
let bobo$= cheerio.load(bohtml_)

//创建沙盒实例
const vm = new VM();

const configCode=fs.readFileSync(`${config_path}/config.js`)
//导入功能插件相关函数
const toolsCode =tools.getCode();
//导入浏览器环境相关
const envCode = env.getCode();
//导入全局初始化
const globalInit = tools.getFile("globalInit");
//导入用户初始化代码
const userInit = tools.getFile( "userInit");
//导入设置代理对象
const proxyObj =  tools.getFile("proxyObj");


//==============================导入需要调试的代码开始 ==============================
const jscode = fs.readFileSync(`${run_path}/tonghuasun.js`)


// ==============================导入需要调试的代码结束==============================


//导入异步执行的代码
const asyncCode = tools.getFile("async");

// bodavm.memory.tag[0].__proto__=HTMLDocument.prototype
//整合代码
//导入日志代码
const log_code=fs.readFileSync(`${tools_path}/printLog.js`)
//测试
const globadlThis=fs.readFileSync(`${tools_path}/globalThis.js`)
// const codeTest=`${configCode}${log_code}${toolsCode}${envCode}${globalInit}${userInit}${changeDom}${proxyObj}${jscode}${asyncCode}`+"\r\n"+"debugger";
const last_deal=fs.readFileSync(`${run_path}/lastDeal.js`)

//导入需要调试的代码
// var jscodess = fs.readFileSync(`${run_path}/xhs.js`)

// const jscodess = fs.readFileSync(`${run_path}/rss.js`)
//沙盒创建全局
vm.setGlobal('bofs', fs)
vm.setGlobal('bobo$',bobo$)
// debugger
vm.setGlobal('bobocheerio',cheerio)
vm.setGlobal('bocreateCanvas',createCanvas)


function ths(){
    const codeTest=`${configCode}${log_code}${toolsCode}${envCode}${globadlThis}${globalInit}${userInit}${proxyObj};;${jscode}${asyncCode};console.table(myloglist);debugger;${last_deal}`
    const script = new VMScript(codeTest, "./debugJS.js")
    const result = vm.run(script);
    console.log(result)
    fs.writeFileSync(`${run_path}/output.js`,codeTest)
}

ths()










