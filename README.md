# WeftWorks

面向服装企业的中英文静态官网。包括首页、圣雪绒款式预览方案、两种语言的错误页，以及原创针织衫 SVG 图稿。没有前端框架、外部字体、分析脚本或运行时依赖。

## 本地启动

```sh
python3 -m http.server 8000 --directory public
```

打开 http://localhost:8000/。这是本机地址，不能直接发给客户。请通过 HTTP 服务器浏览，根路径资源不支持直接双击 HTML 使用 `file://` 浏览。

| 页面 | 中文 | English |
| --- | --- | --- |
| 首页 | `/` | `/en/` |
| 圣雪绒方案 | `/cases/shengxuerong/` | `/en/cases/shengxuerong/` |
| 错误页 | `/404.html` | `/en/404.html` |

导航右侧可切换语言；案例切换后仍停留在案例页。首页切换语言时保留服务、合作方式或关于段落的锚点。默认入口是中文，英文网址可独立分享。语言选择体现在 URL 中，不自动重定向、不写入 Cookie。所有正文和导航在禁用 JavaScript 时也可使用；复制链接是渐进增强功能。

## 文件与更新

- `public/`：完整可部署目录，包含生成后的 HTML 与本地静态资源。
- `scripts/build.py`：两种语言的正文、页面模板与原创 SVG 图稿，使用 Python 标准库。
- `public/assets/site.css`：共用响应式样式；768px 以下采用单列。
- `public/assets/site.js`：复制链接与语言切换时保留锚点。
- `site.config.json`：联系邮箱开关。
- `scripts/check.py`：验证页面结构、站内链接、锚点、资源和必要的事实边界。
- `public/assets/share-cover.png`：1200 × 630 分享封面；同目录 SVG 为可编辑源图。

修改文案或模板后运行：

```sh
python3 scripts/build.py
python3 scripts/check.py
```

把生成后的 `public/` 一起提交。Cloudflare 无需运行生成器。样衣三个配色共享相同 SVG 轮廓、角度与尺寸，分别为雾绿底稿、燕麦色和藏青色。配色不表示实物色号。

## 联系资料

未提供已验证邮箱时，不显示任何联系入口。取得真实业务邮箱并验证后，编辑 `site.config.json`：将 `contact_email` 设为该邮箱，将 `contact_email_verified` 设为 `true`，然后运行生成器并提交输出。两种语言的页脚都会显示可复制地址和邮件草稿入口。不要使用开发者个人邮箱作为占位内容。

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
- 未验证邮箱时不出现 `mailto:`；图注与“方案示意”保留。
- 部署后用未登录窗口及手机打开四个主要路径，并从目标客户常用网络检查图片。此项不能用本地预览替代。

## 内容边界

圣雪绒页面是拟议方案，展示预先制作的原创示意图。没有客户 Logo、实际样衣、员工引语、节省工时或已上线结果，也没有上传、生成、发送功能。Agent 被描述为拟议流程的一部分，最终由设计师和业务员复核。
