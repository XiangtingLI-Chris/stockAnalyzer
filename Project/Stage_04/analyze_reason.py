from __future__ import annotations

def classify_theme(stock_name: str) -> str | None:

    name = str(stock_name).strip()

    # 风险/事件类
    if "退" in name:
        return "退市"
    if "ST" in name:
        return "重组"

    # 金融
    if any(k in name for k in ["券商", "证券"]):
        return "券商"
    if any(k in name for k in ["银行"]):
        return "银行"
    if any(k in name for k in ["保险"]):
        return "保险"

    # 科技
    if any(k in name for k in ["算力", "数据", "服务器", "云", "IDC"]):
        return "算力"
    if any(k in name for k in ["人工智能", "AI", "大模型"]):
        return "AI"
    if any(k in name for k in ["软件", "系统", "信创", "国产", "信息"]):
        return "信创"
    if any(k in name for k in ["通信", "光通信", "5G", "卫星"]):
        return "通信"

    # 半导体/电子
    if any(k in name for k in ["半导体", "芯片", "晶圆", "封装", "EDA"]):
        return "半导体"
    if any(k in name for k in ["电子", "元件", "模组", "电路", "PCB", "显示", "面板"]):
        return "电子"

    # 机器人/自动化/工业母机
    if any(k in name for k in ["机器人", "自动化", "数控", "机床", "工业"]):
        return "制造"

    # 新能源（锂电/储能/光伏/风电）
    if any(k in name for k in ["锂", "电池", "锂电", "正极", "负极", "隔膜", "电解液"]):
        return "锂电"
    if any(k in name for k in ["储能", "逆变器"]):
        return "储能"
    if any(k in name for k in ["光伏", "硅", "组件", "电池片"]):
        return "光伏"

    # 汽车/零部件
    if any(k in name for k in ["汽车", "整车"]):
        return "汽车"
    if any(k in name for k in ["零部件", "轮胎", "轴承", "底盘", "座椅", "内饰"]):
        return "汽车"

    # 医药
    if any(k in name for k in ["创新药", "制药", "药业", "生物"]):
        return "医药"
    if any(k in name for k in ["医疗", "器械", "体外", "IVD"]):
        return "医疗"
    if any(k in name for k in ["疫苗"]):
        return "疫苗"

    # 消费（细分：白酒/食品饮料/旅游酒店/家电/医美）
    if any(k in name for k in ["酒", "白酒", "酒业", "酒类", "酿"]):
        return "酒业"
    if any(k in name for k in ["食品", "饮料", "乳业", "调味", "啤酒"]):
        return "食品"
    if any(k in name for k in ["旅游", "酒店", "餐饮", "免税", "航空"]):
        return "出行"
    if any(k in name for k in ["家电", "电器"]):
        return "电器"
    if any(k in name for k in ["医美", "化妆品", "美容"]):
        return "医美"

    # 资源（有色/煤炭/石油/黄金）
    if any(k in name for k in ["煤", "焦", "炭"]):
        return "煤矿"
    if any(k in name for k in ["石油", "油气", "天然气"]):
        return "油气"
    if any(k in name for k in ["黄金", "金业"]):
        return "黄金"
    if any(k in name for k in ["铜", "铝", "锌", "镍", "稀土", "钴", "锂"]):
        return "有色金属"

    # 化工
    if any(k in name for k in ["化工", "化学", "材料", "塑料", "橡胶"]):
        return "化工"

    # 军工
    if any(k in name for k in ["军", "航天", "航空", "兵器", "船舶"]):
        return "军工"

    # 基建/建筑/建材
    if any(k in name for k in ["基建", "建筑", "工程", "路桥", "建工"]):
        return "建材"
    if any(k in name for k in ["水泥", "建材", "钢构", "玻璃"]):
        return "基建"

    # 地产链
    if any(k in name for k in ["地产", "置业", "开发", "物业"]):
        return "地产"

    # 航运/港口/物流
    if any(k in name for k in ["航运", "港口", "物流", "快递"]):
        return "运价"

    # 农业/养殖
    if any(k in name for k in ["种业", "农业", "饲料", "养殖", "牧", "猪"]):
        return "农产品"

    return None

def month_context(month: int) -> str:
    m = int(month)

    if m == 1:
        return "年初"
    if m == 2:
        return "春节"
    if m == 3:
        return "两会"
    if m == 4:
        return "年报"
    if m in (5, 6):
        return "政策"
    if m in (7, 8):
        return "中报"
    if m == 10:
        return "三季"
    if m in (11, 12):
        return "年末"

    return "窗口"

def heat_tag(hit_times: int | float | None) -> str:
    if heat_tag is None:
        return ""

    try:
        x = float(hit_times)
    except Exception:
        return ""

    if x >= 10:
        return "强势"
    if x >= 6:
        return "活跃"
    if x >= 3:
        return "偏强"

    return "温和"

def analyze_reason(stock_name: str, month: int, hit_times: int | float | None = None) -> str:
    theme = classify_theme(stock_name)
    ctx = month_context(month)
    heat = heat_tag(hit_times)

    if theme == "退市":
        return f"{ctx}博弈风险" if ctx != "窗口" else "博弈风险"
    if theme == "重组":
        mapping = {
            "年初": "重组预期升温",
            "春节": "重组情绪升温",
            "两会": "重组政策预期",
            "年报": "重组进展预期",
            "政策": "重组窗口催化",
            "中报": "重组博弈加剧",
            "兑现": "重组兑现预期",
            "三季": "重组题材轮动",
            "年末": "重组冲刺预期",
        }
        base = mapping.get(ctx, "重组预期升温")
        if heat in ("强势", "活跃"):
            return base.replace("预期", f"{heat}预期")[:10]
        return base[:10]

    if theme:
        action = {
            "年初": "资金配置",
            "春节": "需求催化",
            "两会": "政策预期",
            "年报": "业绩博弈",
            "政策": "政策扰动",
            "中报": "中报预期",
            "兑现": "业绩兑现",
            "三季": "三季预期",
            "年末": "估值轮换",
        }.get(ctx, "轮动催化")

        base = f"{theme}{action}"
        if heat == "强势":
            return (base + "强")[:10]
        if heat == "活跃":
            return (base + "热")[:10]
        return base[:10]

    fallback = {
        "年初": "资金配置",
        "春节": "节后修复",
        "两会": "政策预期",
        "年报": "年报博弈",
        "政策": "政策扰动",
        "中报": "中报预期",
        "兑现": "业绩兑现",
        "三季": "三季预期",
        "年末": "年末切换",
    }.get(ctx, "其他因素")

    if heat == "强势":
        return (fallback + "强")[:10]
    if heat == "活跃":
        return (fallback + "热")[:10]
    if heat == "偏强":
        return (fallback + "稳")[:10]
    return fallback[:10]

# def analyze_reason(stock_name: str, month: int) -> str:
#     """
#     Analyze the reason of a increasing stock.
#     Prioritization: ST/重组 > 行业/题材关键词 > 月份辅助 > 其他原因
#     """
#     name = str(stock_name).strip()
#     m = int(month)
#
#     # ---------- (1) 风险/事件类优先（通常最能解释异常波动）----------
#     if "退" in name:
#         return "退市风险博弈"
#     if "ST" in name:
#         return "重组预期升温"
#     if any(k in name for k in ["N", "C"]) and len(name) <= 6:
#         # 粗糙的“新股”判断
#         return "新股情绪炒作"
#
#     # ---------- (2) 行业/主题细分（尽量覆盖常见A股题材）----------
#     # 金融
#     if any(k in name for k in ["券商", "证券"]):
#         return "券商情绪修复"
#     if any(k in name for k in ["银行"]):
#         return "估值修复驱动"
#     if any(k in name for k in ["保险"]):
#         return "利率预期影响"
#
#     # 科技
#     if any(k in name for k in ["算力", "数据", "服务器", "云", "IDC"]):
#         return "算力需求预期"
#     if any(k in name for k in ["人工智能", "AI", "大模型"]):
#         return "AI题材催化"
#     if any(k in name for k in ["软件", "系统", "信创", "国产", "信息"]):
#         return "信创景气预期"
#     if any(k in name for k in ["通信", "光通信", "5G", "卫星"]):
#         return "通信景气回升"
#
#     # 半导体/电子
#     if any(k in name for k in ["半导体", "芯片", "晶圆", "封装", "EDA"]):
#         return "半导体周期修复"
#     if any(k in name for k in ["设备", "材料"]) and any(k in name for k in ["半导体", "电子", "芯片"]):
#         return "国产替代预期"
#     if any(k in name for k in ["电子", "元件", "模组", "电路", "PCB", "显示", "面板"]):
#         return "消费电子回暖"
#
#     # 机器人/自动化/工业母机
#     if any(k in name for k in ["机器人", "自动化", "数控", "机床", "工业"]):
#         return "制造升级预期"
#
#     # 新能源（锂电/储能/光伏/风电）
#     if any(k in name for k in ["锂", "电池", "锂电", "正极", "负极", "隔膜", "电解液"]):
#         return "锂电链修复"
#     if any(k in name for k in ["储能", "逆变器"]):
#         return "储能景气预期"
#     if any(k in name for k in ["光伏", "硅", "组件", "电池片"]):
#         return "光伏回暖预期"
#
#     # 汽车/零部件
#     if any(k in name for k in ["汽车", "整车"]):
#         return "汽车周期回升"
#     if any(k in name for k in ["零部件", "轮胎", "轴承", "底盘", "座椅", "内饰"]):
#         return "汽车链景气"
#
#     # 医药
#     if any(k in name for k in ["创新药", "制药", "药业", "生物"]):
#         return "医药政策预期"
#     if any(k in name for k in ["医疗", "器械", "体外", "IVD"]):
#         return "医疗需求修复"
#     if any(k in name for k in ["疫苗"]):
#         return "疫苗预期驱动"
#
#     # 消费（细分：白酒/食品饮料/旅游酒店/家电/医美）
#     if any(k in name for k in ["白酒", "酒业", "酒类", "酿"]):
#         return "消费旺季预期"
#     if any(k in name for k in ["食品", "饮料", "乳业", "调味", "啤酒"]):
#         return "消费需求回暖"
#     if any(k in name for k in ["旅游", "酒店", "餐饮", "免税", "航空"]):
#         return "出行复苏预期"
#     if any(k in name for k in ["家电", "电器"]):
#         return "以旧换新预期"
#     if any(k in name for k in ["医美", "化妆品", "美容"]):
#         return "消费升级预期"
#
#     # 资源（有色/煤炭/石油/黄金）
#     if any(k in name for k in ["煤", "焦", "炭"]):
#         return "煤价周期驱动"
#     if any(k in name for k in ["石油", "油气", "天然气"]):
#         return "油气价格驱动"
#     if any(k in name for k in ["黄金", "金业"]):
#         return "避险情绪推升"
#     if any(k in name for k in ["铜", "铝", "锌", "镍", "稀土", "钴", "锂"]):
#         return "有色金属涨价"
#
#     # 化工
#     if any(k in name for k in ["化工", "化学", "材料", "塑料", "橡胶"]):
#         return "化工景气修复"
#
#     # 军工
#     if any(k in name for k in ["军", "航天", "航空", "兵器", "船舶"]):
#         return "军工事件催化"
#
#     # 基建/建筑/建材
#     if any(k in name for k in ["基建", "建筑", "工程", "路桥", "建工"]):
#         return "建材增长预期"
#     if any(k in name for k in ["水泥", "建材", "钢构", "玻璃"]):
#         return "基建链修复"
#
#     # 地产链
#     if any(k in name for k in ["地产", "置业", "开发", "物业"]):
#         return "地产政策预期"
#
#     # 航运/港口/物流
#     if any(k in name for k in ["航运", "港口", "物流", "快递"]):
#         return "运价预期扰动"
#
#     # 农业/养殖
#     if any(k in name for k in ["种业", "农业", "饲料", "养殖", "牧", "猪"]):
#         return "农产品周期"
#
#     # ---------- (3) 月份辅助（假设上述原因均未命中）----------
#     month_reason = {
#         1: "年初资金配置",
#         2: "节后需求预期",
#         3: "政策窗口预期",
#         4: "财报预期博弈",
#         5: "政策预期扰动",
#         6: "资金轮动博弈",
#         7: "中报预期博弈",
#         8: "中报预期博弈",
#         9: "业绩兑现博弈",
#         10: "三季预期博弈",
#         11: "年末行情驱动",
#         12: "估值切换预期",
#     }
#
#     if m in month_reason:
#         return month_reason[m]
#
#     # ---------- (4) 兜底 ----------
#     return "其他原因"
