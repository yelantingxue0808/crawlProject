# vm2 补环境框架（同花顺 JS 逆向）

> 基于 Node.js vm2 沙箱的浏览器环境补全（补环境）框架，用于在 Node 环境中还原浏览器 API，跑通同花顺（tonghuashun）网站 JS 的环境检测与加密逻辑，便于断点调试和逆向分析。

## 项目简介

JS 逆向中常见的做法是"扣代码 + 补环境"：把目标网站加密相关的 JS 扣出来在 Node 里跑，但浏览器代码会检查 `window`、`document`、`navigator`、canvas 指纹等环境，缺了就报错或被检测。本框架解决的就是**在 Node 里把浏览器环境补齐**。

核心思路：

- **vm2 沙箱**：在隔离的 VM 中执行待调试代码，避免污染宿主环境，同时便于注入自定义对象。
- **逐项补环境**：`env/` 目录按浏览器对象逐个补充 API（Document、Element、Event、Canvas、Audio、CookieStore……），缺哪个补哪个。
- **真实 DOM 支撑**：用 cheerio 解析抓取的页面 HTML（`run/run.html`），让 DOM 相关操作有真实文档可依赖。
- **canvas 指纹模拟**：引入 `canvas` 原生模块，模拟浏览器画布指纹，对抗 canvas 指纹检测。
- **代理 + 日志**：通过 `proxyObj`、`printLog` 等工具观察代码对对象的访问行为，辅助逆向定位。

## 目录结构

```
vm2补环境框架/
├── main.js                  # 入口：组装配置/环境/工具/目标代码，创建 vm2 沙箱并运行
├── package.json             # 依赖清单（vm2、cheerio、canvas、fingerprintjs、jssoup 等）
├── package-lock.json        # 依赖锁文件
├── .gitignore               # 忽略 node_modules、build、运行产物等
├── config/                  # 配置文件
│   ├── config.js            # 基础配置（导入哪些模块/代码片段）
│   ├── env.config.js        # 环境补充开关与加载
│   ├── tools.config.js      # 工具模块加载
│   ├── changeDom.js         # DOM 修改/注入逻辑
│   └── json.txt
├── env/                     # 浏览器环境补充（核心）
│   ├── Attr.js              # 每个文件补充一个浏览器对象/API
│   ├── Audio.js
│   ├── CanvasRenderingContext2D.js   # canvas 2D 上下文
│   ├── Document.js / Element.js / Event.js / EventTarget.js ...
│   ├── CookieStore.js / Crypto.js / DOMParser.js ...
│   └── htmlElements/        # HTML 元素相关补充
├── run/                     # 运行目录
│   ├── run.html             # 目标页面 HTML（供 cheerio 解析）
│   ├── tonghuasun.js        # 待调试的目标 JS（同花顺）
│   ├── lastDeal.js          # 收尾处理
│   ├── output.js            # 运行生成的整合调试代码
│   └── log.txt              # 运行日志
├── tools/                   # 辅助工具
│   ├── globalInit.js        # 沙盒全局初始化
│   ├── userInit.js          # 用户自定义初始化
│   ├── proxyObj.js          # 代理对象（观察属性访问/调用）
│   ├── printLog.js          # 日志打印
│   ├── tuodom.js            # DOM 脱钩/处理
│   ├── toolsParseHtml.js / toolsPromise.js / toolsPlugin.js ...
│   └── async.js             # 异步执行支持
├── build/                   # node-gyp 构建产物（本地编译）
└── node_modules/            # 依赖（未纳入仓库，npm install 重建）
```

## 运行方式

1. **安装依赖**：`npm install`

   > `canvas`、`iconv` 等为原生模块，需要 `node-gyp` 编译。Windows 上需安装 VS Build Tools（C++ 构建工具）+ Python。`node_modules/` 未纳入仓库，请按本机环境执行 `npm install` 安装。

2. **准备目标**：
   - 将目标页面 HTML 放到 `run/run.html`
   - 将待调试 JS 放到 `run/tonghuasun.js`（或修改 `main.js` 中的导入路径）

3. **运行**：`node main.js`

4. **查看结果**：
   - `run/output.js`：整合后的完整调试代码（可用 `debugger` 或 IDE 断点调试）
   - `run/log.txt`：运行日志
   - 控制台 `console.table(myloglist)` 输出记录列表

## 学习要点

- **vm2 用法**：`VM` / `VMScript` 的创建与运行，沙箱隔离与注入（`setGlobal`）。
- **补环境思路**：按"报错缺什么补什么"的顺序，逐对象补充 `env/` 下的 API；关注常见检测点——`navigator`、`window`、`document`、canvas 指纹、`Audio`、`EventTarget` 等。
- **DOM 解析**：cheerio 加载真实页面 HTML，配合 DOM API 补充，让代码"有文档可查"。
- **canvas 指纹**：`createCanvas` 模拟浏览器画布行为，应对指纹检测。
- **调试技巧**：`proxyObj` 代理观察属性访问链，`printLog` 记录调用过程，`debugger` 下断点逐行分析。

## 注意事项

- `node_modules/` 按 `.gitignore` 约定未纳入仓库，执行 `npm install` 即可按需重建；`build/` 与 `run/` 内运行产物随项目一并上传，可随时删除。
- 本项目仅用于个人学习与安全研究，请遵守相关法律法规，勿用于非法用途。
