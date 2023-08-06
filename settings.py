"""This file belongs to project 'LIGHTPARTICLE', See README for more detail."""

#  This is not a standalone executable module.

# This file provide some static value of version string. Disable debug output
# with `debug=False`.


# ========================= O P T I O N S ==============================
# - Debugging | 调试开关 -
debug = True                    # 开启调试：True， 关闭：False。
verbose = 5                     # 输出详细等级 {0,5}, 数字越大越详细
line = -1                       # 调试输出单行最大内容长度, -1 无限制
# （推荐） 屏幕窗口行字符长度-38。如窗口 190*80，设置为 190-38 = 152 以内即可

# - Version | 版本信息 -
version = "0.1"

# - MWeb & X-Sec | MWeb 服务版本信息及 X-Sec 配置 -
serv = "2.40.0"                 # 当前适配的 MWeb 版本信息
libmweb = True                  # 使用 MWeb 模块：True， 不使用 False（仅 v0.1）

# - Credential | 登录凭证配置 -
keyfile = ".key"                # 凭证文件 (UA信息与Cookie放在一个文件里的两行中)
cookie = ""                     # 单独配置登录 Cookie
ua = ""                         # 登录时使用的浏览器用户代理（User-Agent）信息
# （如有 key 文件， cookie 与 ua 无需单独重复设定）

# - Download | 下载设置 -
get_download_url = False        # 是否获取文件链接，每日20次限制 - 10631
download_max = 10               # 最大同时下载任务数，最好不好超过电脑 CPU 逻辑核心数
download_thread = 8             # 单个文件的最大并发线程数（建议 8， 过大不可用）
download_interval = 3           # 每个下载任务强制的最大间隔时间（秒 ，实际为[0-x]秒
download_instant = False        # 发现文件资源是否立即下载，或等待信息归并完成再下载。
download_instant_image_only = True  # 即便不下载文件附件，是否仍要下载图片。
# - `True`，逐个，防止链接过期 <链接有效期：图片默认一个月，文件一个小时>
# - `False`，批量，优先内容备份（链接过期后，自动尝试刷新资源链接）
topic_max = 20                  # 单次获取最大获取话题数 <不推荐修改>
comment_max = 30                # 单次获取最大获评论数 <不推荐修改>
file_max = 10                   # 单次获取最大文件数 <不推荐修改>
# （由于存在嵌套的数据管理目录，因此无法静态配置。但可在调用中动态定义修改。默认为当前路径输出）
# 不推荐修改的原因是：即便使用三方工具，行为上也要假装像个正经客户端。这可以规避很多麻烦。
file_verify = True  # 下载文件后，验证文件完整性

# ”Err: 10631“
# 不再盲目下载，而是针对性地寻找内容
# filter_mode = {"keyword": "发财"}  # 文件过滤方案与匹配要素，默认为文件名是否包含关键字。

# 可选的模式列表：
# -- 按文件格式，过滤掉一些大可爱们分享的加密压缩包
# filter_mode = {"format": ["pdf", "pptx"]}

# -- 按文件下载量
# filter_mode = {"trend": True}

# -- 按文件大小 <奇怪现象是，无论是大小还是下载量，前20个结果一样，或许这过滤方式，早都被玩烂了>
# filter_mode = {"size": True}

# -- 文件名+对应帖子文案的内容丰富程度，设置过滤基准值。
# #防止大可爱以后用加密文件名，然后把文件名作为文案随便添及格字继续坑爹。
# filter_mode = {"entropy": True}
# filter_mode = {"entropy": (5.5, )}
# filter_mode = {"entropy": (5.0, 5.3)}
# -- Entropy 过滤见人见智吧，这个我其实也很不确定。

# 如果你喜欢，可以把所有的过滤写一起（放心程序必然是不会慢亿点点的）
# filter_mode = {
#   "keyword": "发财",
#   "format": ["ppt", "pptx", "pdf", "doc", "docx"],
#   "trend": True,
#   "size": True,
#   "entropy": (5.0, )
# }
filter_mode = {
  "keyword": "发财",
  "format": ["ppt", "pptx", "pdf", "doc", "docx"]
  # "trend": True,
  # "size": True
  # "entropy": (5.0, )
}
# - 综合起来的意思就是： 过滤出”讲述关于如何才能发财的不坑爹的附件文件“（显然，结果将会是空）。
# ** 多种条件，综合时默认使用 AND 模式。 对条件结果 List 取 交集。
# 具体表达可以参考 utility.value_attachment 中 #synth. 部分。
# ** 有关稍复杂的链式过滤 utility.value_attachment_chain，因为确实很管用，就不提供了。
# 推荐用递归，不要for in keys！因为 files 是操作参数。

# ”Err: 10631“ - 稍加分析，会感觉大多数据，真的没啥用，如果知识的来源靠营销号，还不如早点去睡觉。

# TODO: Waiting for Implement - Frontend / Export download task and status
# - Render | 前端渲染设置 -
render_pkg = "render.zip"       # 前端（包）位置
render_path = "static/www"      # 渲染前端存放路径
render_avatar = False           # 用户头像是否从远程加载
render_view = 8181              # 内容预览服务端口号 （可任意，默认 0.0.0.0，所有）
render_addr = "0.0.0.0"         # 预览前端服务监听地址
tls_secure = False              # 使用TLS安全技术加密访问（公网部署必须开启）
cert_pem = ""  # HTTPS 证书
cert_key = ""  # HTTPS 证书密钥
export_rss = False              # RSS 订阅文件导出（通过 RSS 方式，推送内容更新消息）

# - Backend | 数据后端配置 -
backend_data = 8182             # 数据服务端口号 (监听位置，127.0.0.1 ， 仅本地)

# - Tasker | 任务相关 -
upload_link = "#"               # 简单的 POST 上传目标位置（可选）
sync_dir = ""                   # 同步盘文件夹路径（可选）
task_interval = 30              # 每多少小时执行一次
task_mode = "cron"              # Linux 系统 crontab 定时任务
task_callback = ""              # 任务执行命令
# （其实这部分应该自己手动配置，要什么选项，而且又没在代码里直接实现完成）

# #========================= E O F ======================================
