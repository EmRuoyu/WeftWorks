# WeftWorks

面向服装企业的中英文静态官网。默认英文，包括首页、独立 About 页面、针织打样案例、两种语言的错误页，以及服装渲染与实物织片对照图。没有前端框架、外部字体、分析脚本或运行时依赖。

## 本地启动

```sh
python3 -m http.server 8000 --directory public
```

打开 [本地首页](http://localhost:8000/)。这是本机地址，不能直接发给客户。请通过 HTTP 服务器浏览，根路径资源不支持直接双击 HTML 使用 `file://` 浏览。

| 页面 | 中文 | English |
| --- | --- | --- |
| 首页 | `/zh/` | `/` |
| About | `/zh/about/` | `/about/` |
| 圣雪绒方案 | `/zh/cases/shengxuerong/` | `/cases/shengxuerong/` |
| 错误页 | `/zh/404.html` | `/404.html` |

导航右侧可切换语言；案例切换后仍停留在案例页。首页切换语言时保留服务、合作方式或关于段落的锚点。默认入口是英文，中文网址可独立分享。旧的 `/en/`、`/en/about/` 和 `/en/cases/shengxuerong/` 仍提供英文页面，保留此前分享链接的可用性。语言选择体现在 URL 中，不自动重定向、不写入 Cookie。所有正文和导航在禁用 JavaScript 时也可使用；复制链接是渐进增强功能。

## 文件与更新

- `public/`：完整可部署目录，包含生成后的 HTML 与本地静态资源。
- `scripts/build.py`：两种语言的正文、页面模板、内容版本化的 CSS/JS 链接与原创 SVG 图稿，使用 Python 标准库。
- `public/assets/site.css`：共用响应式样式；服务卡片在桌面采用四列、中屏两列、手机单列。手机端使用原生可展开菜单。
- `public/assets/site.js`：复制链接、语言切换时保留锚点、手机菜单与一次性入场动效。支持系统减少动态效果偏好，内容不会因 JavaScript 不可用而隐藏。
- `site.config.json`：邮箱、微信号与展示状态。
- `scripts/check.py`：验证页面结构、站内链接、锚点、资源和必要的事实边界。
- `public/assets/share-cover.png`：1200 × 630 分享封面；同目录 SVG 为可编辑源图。

修改文案或模板后运行：

```sh
python3 scripts/build.py
python3 scripts/check.py
```

把生成后的 `public/` 一起提交。Cloudflare 无需运行生成器。首页和案例页使用同一份款式与实物小样对照图，WebP 素材位于 public/assets/polo-*.webp。

## 联系资料

About 页面使用委托方提供的邮箱 `lessthan3@qq.com`，点击即可打开邮件草稿；页脚也显示邮箱入口。微信号为 `WeftWorks_AI`，已由委托方确认开通，页面作为正式联系方式展示。

在 `site.config.json` 中设置 `contact_email` 与 `contact_email_enabled` 来更新邮件入口。`contact_wechat` 为微信号，`contact_wechat_status` 当前是 `active`。修改后运行生成器并提交输出。页面不再展示电话。

## GitHub 与 Cloudflare Pages

仓库： https://github.com/EmRuoyu/WeftWorks

代码存放在 `main`，`review` 分支用于审稿。当前没有绑定 Cloudflare 项目，也没有可交付的公开网站地址。仓库访问权限与网站托管访问权限是两件事。

连接 Cloudflare 的 Workers & Pages → Create application → Pages → Import an existing Git repository，选本仓库：

| 设置 | 填写值 |
| --- | --- |
| Production branch | `main` |
| Framework preset | `None` |
| Build command | 留空；若控制台要求命令，填 `exit 0` |
| Root directory | 仓库根目录（留空） |
| Build output directory | `public` |

保存并部署后，使用控制台返回的实际 `https://<项目名>.pages.dev` 地址，不要自行猜测。推送 `review` 分支后，从部署详情复制 Preview URL。预览地址默认可公开访问，因此只包含可对外展示的内容。审稿确认后合并到 `main`，由 Git 集成自动发布。后续可在 Custom domains 绑定域名；恢复旧版可撤销对应 Git 提交并重新部署。

Cloudflare 使用根目录 `404.html` 返回错误状态；英文专用错误页也可直接访问。站点不配置 SPA fallback，案例和英文页面都有真实目录，支持直接访问和刷新。

官方参考：
- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/
- https://developers.cloudflare.com/pages/configuration/preview-deployments/

## 上线检查

- 在 390px 与 1440px 检查两种语言的首页与案例，没有横向溢出或图片缺失。
- 从首页进入案例、返回服务区、切换语言、刷新案例直链。
- 案例复制按钮显示成功反馈；若浏览器拒绝剪贴板权限，应提示从地址栏复制。
- 各页面包含一个 H1、独立标题和摘要、正确的语言属性；Tab 焦点可见。
- 邮箱链接指向配置的地址；微信号与已确认开通的账号一致；图注区分款式渲染与实物织片。
- 部署后用未登录窗口及手机打开两种语言的首页、About 和案例路径，并从目标客户常用网络检查图片。此项不能用本地预览替代。

## 内容边界

圣雪绒案例展示用户提供的实际打样对照图。上排是款式渲染，下排是实物织片照片。页面提供完整大图及中英文解读。

## FDE 合作方式

About 页末以 Forward Deployed Engineer（前线部署工程师）解释合作思路：贴近业务团队，理解一项真实工作，共同开发小版本，再接入系统并迭代。它描述我们的合作方法，不代表已完成的客户项目或业绩承诺。术语参考：[Palantir 官方职位说明](https://jobs.lever.co/palantir/5168e8fd-fec1-4fea-b7a1-81bdaea65850)。
