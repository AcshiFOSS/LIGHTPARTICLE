"""This file belongs to project 'LIGHTPARTICLE', See README for more detail."""

# Module `LIGHTPARTICLE.error` containing some data from *.js on api.zsxq.com.
# We are using those date for handling application errors.

from settings import debug
from utility import bl4th3r


def ENOZSXQ(code) -> str:
    """
    Convert API error to readable message. (PEP-634 style, Python 3.10+)
    List of API error code from: main.js on zsxq.com <MWeb@2.39.0>
    param:
      - <int> code   error code.
    """
    match code:
        case 1:
            return "非法json格式"
        case 2:
            return "停止服务"
        case 3:
            return "停止服务提示"
        case 200:
            return "请求成功"
        case 404:
            return "没有找到资源"
        case 401:
            # return "未认证"
            return "未认证，或资源下载链接已过期"  # Modified for request directly.
        case 403:
            return "禁止访问"
        case 404:
            return "资源位置错误"  # Add for blob。
        case 500:
            return "内部错误"
        case 600:
            return "web api 请求app后端服务器失去响应"
        case 1001:
            return "无效的end_time"
        case 1002:
            return "无效的begin_time"
        case 1003 | 14204 | 14401 | 17802 | 17802:
            return "count超出范围"
        case 1004:
            return "参数错误"
        case 1005:
            return "登录的用户不是星球成员"
        case 1006:
            return "用户不是星球管理员"
        case 1007:
            return "主题已被删除"
        case 1008:
            return "关键查询用户不是星球成员"
        case 1009:
            return "用户被踢下线"
        case 1010:
            return "无效的关键词大小"
        case 1011:
            return "该用户已被拉黑"
        case 1012:
            return "post请求缺少body"
        case 1013:
            return "相同request_id的创建操作，处理失败"
        case 1014 | 14001 | 17801 | 17801:
            return "无效的count"
        case 1015:
            return "身份验证失败，参考交互协议。"
        case 1016:
            return "数据库操作失败"
        case 1017:
            return "提问未被回答，不允许该操作"
        case 1018 | 12201:
            return "无效的sort"
        case 1019:
            return "用户不是圈主"
        case 1020:
            return "无效的filter"
        case 1021:
            return "无效的order"
        case 1022:
            return "评论不存在或已被删除"
        case 1023:
            return "用户被禁言"
        case 1024 | 1034:
            return "用户没有提交过实名资料"
        case 1025:
            return "订单号已经被使用"
        case 1026:
            return "发表失败，内容非法"
        case 1027:
            return "没有续期，内容过期"
        case 1028 | 1029:
            return "没有绑定手机"
        case 1030 | 15404:
            return "没有权限"
        case 1031:
            return "用户不存在"
        case 1032:
            return "用户头像不存在"
        case 1033:
            return "缺少关键参数"
        case 1035:
            return "帮助星球不允许该请求"
        case 1036:
            return "体验卡用户只可查看最新30天内容"
        case 1037:
            return "用户已经退出星球"
        case 1038:
            return "永久类型星球不允许该请求"
        case 1039:
            return "免费体验成员不允许该请求"
        case 1040:
            return "数据库唯一键冲突"
        case 1041 | 15101:
            return "无效的topic_id"
        case 1042:
            return "无效的comment_id"
        case 1043:
            return "无效的url"
        case 1046:
            return "高风险星球，不允许该请求"
        case 1047:
            return "禁止分享主题的星球，不允许该请求"
        case 1048:
            return "暂不允许发起写请求"
        case 1049:
            return "审核中的主题"
        case 1056:
            return "面额超出范围"
        case 1057:
            return "无效名称"
        case 1059:
            return "X-Signature 校验失败"  # Oops. That's not so good.
        case 10004:
            return "未找到登录方式"
        case 10005:
            return "未找到email"
        case 10006:
            return "无效的union_id"
        case 10007:
            return "无效的device_id"
        case 10008:
            return "无效的device_name"
        case 10009:
            return "用户被封号"  # Oops. Contact support.zsxq.com, no other ways.
        case 10010:
            return "redis服务器错误"
        case 10011:
            return "更新用户登录信息失败"
        case 10012:
            return "未找到union_id"
        case 10013:
            return "未找到用户"
        case 10014:
            return "获取微信token网络错误"
        case 10015:
            return "获取微信token数据错误"
        case 10016:
            return "获取微信userinfo网络错误"
        case 10017:
            return "生成access_token错误"
        case 10018:
            return "创建用户失败"
        case 10019:
            return "无效的appid"
        case 10020:
            return "获取用户的微信昵称失败"
        case 10021:
            return "无效的client_time"
        case 10022:
            return "无效的验证码信息"
        case 10023:
            return "密码错误次数太多，30分钟内禁止登录"
        case 10024:
            return "(LP) 不允许获取评论或星主关闭该话题评论"
        case 10201:
            return "注销成功"
        case 10202:
            return "注销失败"
        case 10304:
            return "未找到文件信息"
        case 10305:
            return "用户没有在指定星球内"
        case 10501:
            return "无效的remark"
        case 10503:
            return "未找到remark"
        case 10801:
            return "无效的name"
        case 10802:
            return "无效的avatar_id"
        case 10803:
            return "avatar_id无效范围"
        case 10804:
            return "更新个人信息失败"
        case 10805:
            return "更新用户信息失败"
        case 10806:
            return "获取文件相关信息失败"
        case 10807:
            return "无效的头像文件"
        case 10901:
            return "用户已经绑定"
        case 10902:
            return "微信已经被绑定到另一个账户"
        case 10903:
            return "获取微信信息失败"
        case 11101:
            return "加入星球时，服务端错误"
        case 11102:
            return "没有找到这个星球"
        case 11103:
            return "当前时间超过会员截止时间"
        case 11104:
            return "生成审批信息失败"
        case 11105:
            return "第一次加入付费星球，需要提供支付订单"
        case 11106:
            return "订单不存在或没有支付"
        case 11107:
            return "星球不允许加入"
        case 11110:
            return "试运营星球加入人数超限"
        case 11111:
            return "过期未续期的不能加入星球或购买礼品卡"
        case 11301:
            return "无效的status"
        case 11302:
            return "无效的examination_ids"
        case 11303:
            return "加入审批星球失败"
        case 11304:
            return "更新审批星球失败"
        case 11305 | 12001 | 14201 | 14801:
            return "无效的group_id"
        case 11401:
            return "无效的group_name"
        case 11402:
            return "group_background_url长度无效"
        case 11403:
            return "无效的group_background_url"
        case 11404:
            return "无效的policies"
        case 11405:
            return "无效的examine_type"
        case 11406 | 11503 | 16902:
            return "无效的amount"
        case 11407 | 11505:
            return "无效的duration"
        case 11408:
            return "加入星球失败"
        case 11409:
            return "创建星球失败"
        case 11410:
            return "无效的cover_color"
        case 11411:
            return "cover_color不是颜色格式"
        case 11412:
            return "无效的category_id"
        case 11413:
            return "添加星球分类失败"
        case 11501 | 15103:
            return "获取星球信息失败"
        case 11502:
            return "无效的背景图链接"
        case 11504:
            return "amount超出范围"
        case 11506 | 14809:
            return "无效的type"
        case 11507:
            return "当星球成员数目大于500时，星球成员只能管理员可见"
        case 11508:
            return "获取星球关系失败"
        case 11509:
            return "更新星球信息失败"
        case 11510:
            return "user_id或group_id错误"
        case 11511:
            return "没有参数"
        case 11512:
            return "polices无效"
        case 11513:
            return "无效的管理员id"
        case 11514:
            return "星球名长度错误"
        case 11515:
            return "星球背景颜色错误"
        case 11516:
            return "category_id不存在"
        case 11601:
            return "获取偏好失败"
        case 11701:
            return "alias超出长度限制"
        case 11702:
            return "无效的accept_dynamics"
        case 11703:
            return "无效的accept_message_notifications"
        case 11704:
            return "更新数据库失败"
        case 11705:
            return "必须指定一个参数"
        case 12402:
            return "获取成员信息失败"
        case 12501:
            return "获取成员关系失败"
        case 12601:
            return "获取成员排名失败,服务端错误"
        case 12901:
            return "更新圈主失败"
        case 12902 | 13004:
            return "删除成员失败"
        case 12903:
            return "圈主不能退出还有成员的付费星球"
        case 13001:
            return "不能移除自己"
        case 13002:
            return "用户不在星球里"
        case 13003:
            return "没有权限移除成员"
        case 13101:
            return "无效的image_type"
        case 13102:
            return "无效的image_hash"
        case 13301:
            return "无权限访问该文件信息"
        case 13302:
            return "无法找到该文件"
        case 13401:
            return "无效的file_name"
        case 13402:
            return "无效的file_hash"
        case 13403:
            return "文件服务器错误"
        case 13404:
            return "文件类型不支持"
        case 13501:
            return "请求api失败"
        case 13502:
            return "上传文件不存在或hash值与预上传hash值不一致"
        case 13503:
            return "上传文件超过30M"
        case 13504:
            return "图片类型不支持"
        case 13601:
            return "禁止访问文件"
        case 13602:
            return "文件不存在"
        case 13603:
            return "文件地址获取失败，导致不能获取文件预览地址"
        case 13604:
            return "文件预览服务器返回错误"
        case 13607:  # Add by us.
            return "(LP) 超过当日文件下载数量上限"  # Be calm and understanding。。。
        case 13701:
            return "没有找到文件"
        case 14205:
            return "获取用户动态失败"
        case 14206 | 15102 | 15501:
            return "获取主题信息失败"
        case 14207 | 17210:
            return "星球已经锁定"
        case 14209:
            return "星球是高风险星球"
        case 14210:
            return "成员体验已到期"
        case 14701:
            return "未找到标签"
        case 14802:
            return "无效的image_ids"
        case 14803:
            return "无效的file_ids"
        case 14804:
            return "无效的content"
        case 14805:
            return "主题内容超出长度限制"
        case 14806 | 15303:
            return "@ 的用户不存在"
        case 14808:
            return "创建主题服务器错误"
        case 14810:
            return "无效的questionee_id"
        case 14811:
            return "创建提问text长度超出限制"
        case 14812:
            return "anonymous无效，不是bool值"
        case 14813:
            return "questionee_id不是圈主或嘉宾id"
        case 14814:
            return "订单号不存在或者订单金额小于1分钱或者订单已经创建过提问"
        case 14815:
            return "创建提问服务器错误"
        case 14816:
            return "订单已经退款"
        case 14817:
            return "标签长度超出范围"
        case 14818:
            return "全空标签"
        case 14901:
            return "没有权限删除主题"
        case 14902:
            return "删除主题错误"
        case 14903:
            return "已完成的提问任何人无法删除"
        case 14904:
            return "付费的提问过期之前无法删除"
        case 14905:
            return "免费提问只有创建者可以删除"
        case 15001:
            return "未找到主题"
        case 15201:
            return "置顶主题失败"
        case 15202:
            return "sticky参数错误"
        case 15203:
            return "tag长度超出范围"
        case 15204:
            return "空标签"
        case 15301:
            return "无效的text"
        case 15302:
            return "text超出长度限制"
        case 15304:
            return "创建评论失败"
        case 15305:
            return "无效的replied_comment_id"
        case 15306:
            return "无效的repliee_id"
        case 15307:
            return "空的评论内容"
        case 15308:
            return "被回复的评论不存在"
        case 15309:
            return "被回复的成员不在星球内"
        case 15310:
            return "图片不存在"
        case 15311:
            return "父评论被删除"
        case 15401:
            return "获取主题评论失败"
        case 15402 | 17702:
            return "评论已经被删除"
        case 15403 | 17704:
            return "主题已经被删除"
        case 15405:
            return "删除评论失败"
        case 15504:
            return "更新主题信息失败"
        case 15505:
            return "创建点赞失败"
        case 16001:
            return "连接es服务器失败"
        case 16101:
            return "缺少关键词"
        case 16102:
            return "es请求超时"
        case 16103:
            return "es请求错误"
        case 16104:
            return "无效的index"
        case 16202:
            return "无效的count范围"
        case 16203:
            return " 连接es服务器失败"
        case 16204:
            return "es服务器返回错误"
        case 16701:
            return "无效的logined_to_message_server"
        case 16801:
            return "通过transaction_id查询数据库失败"
        case 16802:
            return "交易记录不属于当前用户"
        case 16901:
            return "amount不是数字"
        case 16903:
            return "账户余额不足"
        case 16904:
            return "该用户没有获取开放平台和公众平台的open_id"
        case 16905:
            return "提现过于频繁"
        case 16906:
            return "创建订单号失败"
        case 16907:
            return "更新金额失败"
        case 16908:
            return "您今日的提现次数超过限制"
        case 16909:
            return "短时间内提现过于频繁，请稍后重试"
        case 16910:
            return "提现金额不能小于微信最低限额1元"
        case 16911:
            return "Openid格式错误或者不属于商家公众账号"
        case 16912:
            return "内部错误: 1"
        case 16913:
            return "微信系统繁忙，请稍后再试。"
        case 16914:
            return "内部错误: 2"
        case 16915:
            return "内部错误: 3"
        case 16916:
            return "提现金额不能超过可用金额（可用金额 = 总资产 - 冻结金额）"
        case 17001:
            return "无效的useragent"
        case 17101:
            return "不能自己隔离自己"
        case 17102:
            return "隔离成员失败"
        case 17202:
            return "获取微信预付单失败"
        case 17203:
            return "web api获取费用信息失败"
        case 17204:
            return "web api不是收费圈"
        case 17205:
            return "web api是圈内成员"
        case 17206:
            return "创建订单号type错误"
        case 17207:
            return "创建订单号group_id错误"
        case 17208:
            return "星球不存在或不是付费星球"
        case 17209:
            return "amount必须等于星球价格"
        case 17211:
            return "高风险星球禁止加入"
        case 17212:
            return "非圈内成员不能邀请用户加入星球"
        case 17213:
            return "已存在支付的入圈订单"
        case 17214:
            return "创建订单号topic_id错误"
        case 17215:
            return "还在有效期内，不需要续期"
        case 17216:
            return "提问未被回答，非全员可见状态"
        case 17217:
            return "创建订单号amount错误"
        case 17218:
            return " 不可加入（由于你之前被星主移除，只有被邀请为嘉宾才可加入）"
        case 17219:
            return "开启了审核的星球不可购买礼品卡"
        case 17220:
            return "没有权限续期，不在星球内，体验用户，被删除"
        case 17221:
            return "多次退款，不允许再次加入星球"
        case 17301:
            return "语音长度必选项"
        case 17302:
            return "语音长度必须在[1, 120]之间"
        case 17303:
            return "数据库交互异常"
        case 17304:
            return "请求sapi失败"
        case 17401:
            return "语音长度超出限制"
        case 17402:
            return "没有找到相关语音内容"
        case 17403:
            return "创建回答出错，服务端错误"
        case 17404:
            return "不是问答型主题"
        case 17405:
            return "不是指定的回答者"
        case 17406:
            return "已经回答过该主题（问题）了"
        case 17501:
            return "星球已经删除（解散）"
        case 17502:
            return "生成嘉宾邀请链接失败"
        case 17601:
            return "不支持的媒体类型"
        case 17602:
            return "语音不存在"
        case 17603:
            return "语音已经被删除"
        case 17701:
            return "评论不存在"
        case 17703:
            return "主题不存在"
        case 17901 | 17901:
            return "设置嘉宾错误"
        case 17902 | 17902:
            return "不能把自己设置为嘉宾"
        case 18001:
            return "style参数错误"
        case 18002:
            return "sort参数错误"
        case 18003:
            return "获取/设置个人偏好错误"
        case 18101:
            return "跟评论不存在或已经被删除"
        case 19001 | 50001:
            return "curl 请求失败"
        case 19002 | 50002:
            return "星球拒绝访问"
        case 19003 | 50003:
            return "curl 请求后端失败"
        case 19101:
            return "星球被删除（解散）"
        case 19201 | 50201:
            return "无效的嘉宾标示"
        case 19202 | 50202:
            return "圈主不能成为嘉宾"
        case 1044 | 50203:
            return "要加入的星球不存在"
        case 19204 | 50204:
            return "已经是嘉宾"
        case 19205 | 50205:
            return "错误的邀请token"
        case 19301:
            return "无效的scope值"
        case 21500:
            return "草稿不存在"
        case 21501:
            return "草稿数超过了限制"
        case 21502:
            return "标题长度过长"
        case 21503:
            return "内容长度过长"
        case 21504:
            return "长文章不存在或者被删除"
        case 50101:
            return "星球被删除"
        case 50102:
            return "找不到星球"
        case 50206:
            return "超过嘉宾数量限制"
        case 50207:
            return "合伙人"
        case 50401:
            return "传入的url参数有误"
        case 50402:
            return "获取权限验证配置失败"
        case 18101:
            return "主题被删除"
        case 50501:
            return "星球禁止搜索和分享"
        case 50601:
            return "高风险星球"
        case 50602:
            return "锁定星球"
        case 51401:
            return "推送内容长度不合法"
        case 51402:
            return "推送链接标题长度不合法"
        case 51403:
            return "跳转链接域名不合法"
        case 51404:
            return "一天只能申请一次"

        case _:
            if debug:
                bl4th3r("debug", "Unknown err: " + str(code))
            return "未知错误 (Contact LIGHTPARTICLE team for technical support!)"
