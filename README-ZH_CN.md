LIGHTPARTICLE - 备份线上的数据内容以便您“稍后离线阅读“ | [English](README.md)

没有额外的外部模块依赖。
无需数据库（File-Flatted）的。
丰富的配置参数。

## 使用帮助

下载本工程的源代码，进入该目录：

> ./LIGHTPARTICAL

更多使用选项，请参考[settings.py](settings.py)文件。
我们不会在开源平台上无偿提供任何 `开箱即用` 的工具或程序，出于对具体用途不确定性的担忧。


## 路径与文件说明

```
LIGHTPARTICLE                             # 工程主路径 $HOMEDIR$
├── doc                                   # 部分手册 与 由 `pdoc`自动导出的 APIDoc 
├── libmweb-linux-2.40.0                  # MWeb 工具库（Linux 版）
├── static                                # 静态资源文件
│   ├── certs                             # 本地服务的 HTTPS 证书
│   ├── data                              # 默认备份文件存储位置
│   └── www                               # 前端 (*.html; *.js; etc.) 文件路径
| ...(omit)...                            # LIGHTPARTICLE 必要模块
└── testing                               # 测试用例及批量测试工具

```

代码内已经提供了可动态配置的参数 `basedir` 和 `dirname`，用于指定静态资源文件的存储目录结构。
可以根据实际需要，进行目录结构的设计，方便进行后续的数据分析与操作。

## 测试

为了方便进行测试，我们设计并实现了简单的单元测试执行模块。有关已有的测试用例、测试用例编写方法、
用例注册与批量执行等细节说明，请参考[本工程文档](doc)目录下的文件。

## 开发须知

即便我们尽可能地使用仅依赖 Python 的原生实现，避免对第三方模块的大量使用，简化开发环境安装与部
署。在实际的开发过程中，仍建议安装使用 Pycharm 提供的代码分析工具与模块。以便清楚地理解部分代
码块间的关系、运行时的动态调试。

以下功能是我们没有进行额外引用的功能，可能会在遇到问题时，对实际的调试带来一定困扰：
- 替代对 logging 模块的封装，提供简化的日志输出 `utility.bl4th3r(level, msg)`
  - 阻塞式的
  - 未提供文件句柄（file-handler）输出日志到文件
  - 日志 level 可能改变程序运行状态（例如 `critical` 会触发 `SystemExit` 终止执行）
  - 缺乏更有效的过滤选项，输出较冗杂
 
- 避免额外了解 unittest 带来的额外学习成本，提供 [testing.py](testing/testing.py) 工具
  - 由于使用异常处理对无法找到的`testcase`进行提示和处理，用例中触发的深层级异常可能无法抛出

- 请求处理部分采用 C/Python 混编方式
  - 此部分未公开源代码，调试存在困难
  - 已提供的二进制文件编译参数中未添加调试相关配置，库文件无法直接调试
  - 即便已经使用全静态（full-static）方式构建，仍会存在包括系统兼容问题等其他未知的异常

欢迎任何形式的PR，分享您的创意。

## 声明

您可能需要借助本工程中的代码片段、模块，编写您所需要的操作。由您所二次创作的代码内容，与本组织无
关，我们不对您的创作、您的后续行为，承担任何的附加责任，也不会进一步提供额外的技术支持。

工具并非官方应用，代码内已提供的方法，可能因官方平台应用后续的版本更新，而无法使用。

根据“平台”（*.zsxq.com）规则的要求，即便您使用本仓库中的代码构建所需功能，任何您所下载的已购
数据，仅可用于您个人离线阅读浏览使用。请勿侵犯内容发布者的平台权益，“任何下载均记录在案”，二次
传播您已付费但仅拥有浏览权限的数据内容，是不被“平台”允许的。