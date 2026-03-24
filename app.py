import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
from datetime import datetime
from pathlib import Path
import os
import sys

st.set_page_config(
    page_title="解码“她”的数据｜珀莱雅精准营销智能决策系统",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def configure_console_encoding():
    # Windows 终端兜底：避免中文状态日志出现乱码
    if os.name == "nt":
        try:
            os.environ["PYTHONIOENCODING"] = "utf-8"
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
            if hasattr(sys.stderr, "reconfigure"):
                sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

configure_console_encoding()

def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --text: #eef7ff;
            --muted: #a8c8de;
            --primary-color: #2563eb;
        }
        .stApp {
            --primary-color: #2563eb !important;
            background:
                radial-gradient(circle at 20% 20%, rgba(77,170,255,0.18), transparent 28%),
                radial-gradient(circle at 80% 0%, rgba(125,227,214,0.18), transparent 24%),
                linear-gradient(135deg, #04111f 0%, #08213e 38%, #0d2e57 68%, #123865 100%);
            color: var(--text);
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        .block-container { padding-top: 0.4rem; padding-bottom: 2rem; }
        h1, h2, h3, h4, h5 { color: var(--text) !important; }

        /* 按钮样式 */
        div.stButton > button {
            background: linear-gradient(135deg, #0d2e57, #123865);
            border: 1px solid rgba(132, 211, 255, 0.2);
            border-radius: 14px;
            color: #eef7ff;
            font-weight: 500;
            padding: 12px 14px;
            width: 100%;
            margin-bottom: 8px;
        }
        div.stButton > button:hover {
            background: linear-gradient(135deg, #1a4a8a, #2062a8);
            border-color: rgba(132, 211, 255, 0.4);
        }

        /* ====================== 下拉框终极美化 ====================== */
        /* 输入框背景（淡蓝） */
        div[data-baseweb="select"] > div {
            background-color: #eaf4ff !important;
            border: 1px solid #bfdbfe !important;
            border-radius: 10px !important;
        }
        /* 下拉框内已选值文字改为蓝色，避免看不见 */
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div[role="combobox"],
        div[data-baseweb="select"] input {
            color: #1d4ed8 !important;
            -webkit-text-fill-color: #1d4ed8 !important;
            font-weight: 600 !important;
        }
        /* 兼容 BaseWeb 单选值容器，防止选中后变白字 */
        div[data-baseweb="select"] [class*="singleValue"],
        div[data-baseweb="select"] [class*="SingleValue"],
        div[data-baseweb="select"] [class*="valueContainer"],
        div[data-baseweb="select"] [class*="ValueContainer"] {
            color: #1d4ed8 !important;
            -webkit-text-fill-color: #1d4ed8 !important;
            opacity: 1 !important;
        }
        /* 再次强制：下拉框里展示出来的已选值必须是蓝色 */
        [data-testid="stSelectbox"] [data-baseweb="select"] *,
        [data-testid="stSelectbox"] [data-baseweb="select"] div,
        [data-testid="stSelectbox"] [data-baseweb="select"] span,
        [data-testid="stSelectbox"] [data-baseweb="select"] input {
            color: #1d4ed8 !important;
            -webkit-text-fill-color: #1d4ed8 !important;
            opacity: 1 !important;
        }

        /* 强制显示下拉箭头 */
        svg[fill="none"][stroke="currentColor"] {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            stroke: #1d4ed8 !important;
        }

        /* 下拉面板 */
        div[role="listbox"] {
            background-color: #eaf4ff !important;
            border: 1px solid #bfdbfe !important;
            border-radius: 10px !important;
        }

        /* 选项文字颜色 */
        div[role="option"] {
            color: #1e40af !important;
            background-color: #eaf4ff !important;
        }

        /*  hover 效果 */
        div[role="option"]:hover {
            background-color: #dbeafe !important;
            color: #1d4ed8 !important;
        }

        /* 选中项 —— 无背景，只留蓝色文字 */
        div[role="option"][aria-selected="true"] {
            background-color: #dbeafe !important;
            color: #2563eb !important;
            font-weight: 600 !important;
        }

        /* 让下拉框显示明显箭头标识 */
        div[data-baseweb="select"] > div {
            position: relative;
            padding-right: 34px !important;
        }
        div[data-baseweb="select"] > div::after {
            content: "▼";
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #1d4ed8;
            font-size: 12px;
            pointer-events: none;
        }

        /* 高级筛选区域淡蓝底 */
        [data-testid="stExpander"] details,
        [data-testid="stExpander"] details > div,
        [data-testid="stExpander"] details > div > div {
            background: #eaf4ff !important;
            border: 1px solid #bfdbfe !important;
            box-shadow: none !important;
        }
        /* 仅顶部折叠条改成科技蓝 */
        [data-testid="stExpander"] summary {
            background: linear-gradient(135deg, #0d2e57, #123865) !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            border: 1px solid rgba(132, 211, 255, 0.25) !important;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary *,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span {
            color: #ffffff !important;
        }
        [data-testid="stExpander"] summary:hover {
            background: linear-gradient(135deg, #1a4a8a, #2062a8) !important;
        }

        /* 修复筛选框标题文字可见性 */
        [data-testid="stExpander"] label,
        [data-testid="stExpander"] .stMarkdown,
        [data-testid="stExpander"] p {
            color: #0f2f57 !important;
            font-weight: 600 !important;
        }

        /* 去掉多选标签的红色块，只保留文字 */
        span[data-baseweb="tag"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #1e40af !important;
        }
        span[data-baseweb="tag"] > span {
            color: #1e40af !important;
        }

        /* 滑块背景 */
        div[data-testid="stSlider"] {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 8px 12px;
            --primary-color: #2563eb !important;
            --secondary-background-color: #93c5fd !important;
        }
        div[data-testid="stSlider"] [data-baseweb="slider"] {
            --primary-color: #2563eb !important;
            --secondary-background-color: #93c5fd !important;
        }
        /* 年龄滑块改成蓝色（轨道+填充+圆点） */
        div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
            background-color: #2563eb !important;
            border-color: #2563eb !important;
        }
        div[data-testid="stSlider"] [data-baseweb="slider"] div[role="presentation"] > div {
            background-color: #93c5fd !important;
        }
        div[data-testid="stSlider"] [data-baseweb="slider"] div[role="presentation"] > div > div {
            background-color: #2563eb !important;
        }
        /* 兼容原生 range 样式：整条线改蓝 */
        [data-testid="stSlider"] input[type="range"] {
            accent-color: #2563eb !important;
        }
        [data-testid="stSlider"] input[type="range"]::-webkit-slider-runnable-track {
            background: #93c5fd !important;
        }
        [data-testid="stSlider"] input[type="range"]::-webkit-slider-thumb {
            background: #2563eb !important;
            border: 1px solid #2563eb !important;
        }
        [data-testid="stSlider"] input[type="range"]::-moz-range-track {
            background: #93c5fd !important;
        }
        [data-testid="stSlider"] input[type="range"]::-moz-range-progress {
            background: #2563eb !important;
        }
        [data-testid="stSlider"] input[type="range"]::-moz-range-thumb {
            background: #2563eb !important;
            border: 1px solid #2563eb !important;
        }
        /* 兜底：覆盖 Streamlit 默认红色主色内联样式 */
        div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="rgb(255, 75, 75)"],
        div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="rgba(255, 75, 75"],
        div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="#ff4b4b"],
        div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="255,75,75"] {
            background: #2563eb !important;
            background-color: #2563eb !important;
            border-color: #2563eb !important;
            box-shadow: none !important;
        }
        /* 终极兜底：全局把 Streamlit 默认红色主色替换为蓝色 */
        .stApp [style*="rgb(255, 75, 75)"],
        .stApp [style*="rgba(255, 75, 75"],
        .stApp [style*="#ff4b4b"],
        .stApp [style*="255,75,75"] {
            background-color: #2563eb !important;
            border-color: #2563eb !important;
            color: #2563eb !important;
        }
        .stApp [style*="rgb(255, 75, 75)"] svg,
        .stApp [style*="rgba(255, 75, 75"] svg,
        .stApp [style*="#ff4b4b"] svg {
            fill: #2563eb !important;
            stroke: #2563eb !important;
        }
        /* 年龄区标题和其它筛选标题统一 */
        .filter-label {
            color: #0f2f57 !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            line-height: 1.25 !important;
            margin-bottom: 0.15rem !important;
        }
        /* ============================================================ */

        .hero-box {
            background: linear-gradient(135deg, rgba(9, 39, 73, 0.90), rgba(13, 56, 101, 0.82));
            border: 1px solid rgba(132, 211, 255, 0.16);
            border-radius: 24px; padding: 26px 28px 22px 28px;
            box-shadow: 0 18px 40px rgba(0,0,0,0.22); backdrop-filter: blur(10px);
            margin: 0 0 18px 0;
        }
        .hero-box h1 {
            margin: 0;
            text-align: center;
        }
        .glass-card {
            background: rgba(10, 33, 61, 0.66);
            border: 1px solid rgba(132, 211, 255, 0.14);
            border-radius: 22px; padding: 18px 18px 16px 18px;
            box-shadow: 0 10px 28px rgba(0,0,0,0.16); backdrop-filter: blur(12px);
        }
        .metric-card {
            background: linear-gradient(180deg, rgba(10, 33, 61, 0.84), rgba(8, 29, 53, 0.86));
            border: 1px solid rgba(132, 211, 255, 0.14); border-radius: 22px;
            padding: 18px 18px 14px 18px; min-height: 120px; box-shadow: 0 10px 24px rgba(0,0,0,0.14);
        }
        .metric-label { color: var(--muted); font-size: 0.95rem; margin-bottom: 10px; }
        .metric-value { color: var(--text); font-size: 2rem; font-weight: 700; line-height: 1.1; }
        .metric-sub { color: #8de9d6; font-size: 0.88rem; margin-top: 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

PALETTE = {
    "敏感型": "#57c7ff",
    "自然转化型": "#7de3d6",
    "反作用型": "#ff8c9b",
    "核心价值用户": "#57c7ff",
    "潜力发展用户": "#87a8ff",
    "高价值沉睡用户": "#ffd79a",
    "低价值/流失用户": "#ff8c9b",
    "源力系列": "#7de3d6",
    "红宝石系列": "#d6b7ff",
    "双抗系列": "#57c7ff",
    "基础保湿系列": "#87a8ff",
    "能量系列": "#ffd79a",
}

SERIES_KEYWORDS = {
    "红宝石系列": ["红宝石"],
    "双抗系列": ["双抗", "早C晚A"],
    "源力系列": ["源力", "神经酰胺", "安瓶"],
    "能量系列": ["能量", "赋能鲜颜", "紧致"],
    "基础保湿系列": ["保湿", "水乳", "精华水", "面霜", "洁面", "防晒"],
}

SKIN_SERIES_PREFERENCE = {
    "敏感肌": {"源力系列": 0.95, "红宝石系列": 0.30, "双抗系列": 0.40, "能量系列": 0.20, "基础保湿系列": 0.50},
    "油性/混油": {"源力系列": 0.40, "红宝石系列": 0.50, "双抗系列": 0.85, "能量系列": 0.30, "基础保湿系列": 0.50},
    "干性/混干": {"源力系列": 0.60, "红宝石系列": 0.85, "双抗系列": 0.40, "能量系列": 0.50, "基础保湿系列": 0.70},
    "中性": {"源力系列": 0.50, "红宝石系列": 0.60, "双抗系列": 0.60, "能量系列": 0.50, "基础保湿系列": 0.60},
}

CONCERN_BOOST = {
    "敏感泛红": {"源力系列": 0.20},
    "细纹皱纹": {"红宝石系列": 0.20, "能量系列": 0.10},
    "暗沉发黄": {"双抗系列": 0.20},
    "松弛下垂": {"能量系列": 0.20, "红宝石系列": 0.10},
    "干燥缺水": {"基础保湿系列": 0.15, "源力系列": 0.10},
    "综合护理": {},
}

def metric_card(title, value, sub):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def to_excel_bytes(df_dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, d in df_dict.items():
            d.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    return output.getvalue()

def detect_series(name):
    text = str(name)
    for series, keywords in SERIES_KEYWORDS.items():
        for k in keywords:
            if k in text:
                return series
    return "其他系列"

@st.cache_data
def build_demo_data(n=1600, seed=42):
    rng = np.random.default_rng(seed)
    user_ids = [f"PLY{100000+i}" for i in range(n)]
    uplift_type = rng.choice(["敏感型", "自然转化型", "反作用型"], size=n, p=[0.30, 0.693, 0.007])
    gender = rng.choice(["女", "男"], size=n, p=[0.70, 0.30])
    province = rng.choice(["广东", "浙江", "江苏", "北京", "上海", "山东", "四川", "福建", "湖北", "湖南"], size=n)
    skin_type = rng.choice(["敏感肌", "油性/混油", "干性/混干", "中性"], size=n, p=[0.351, 0.279, 0.219, 0.151])
    member = rng.choice(["是", "否"], size=n, p=[0.47, 0.53])
    age = np.clip(rng.normal(32, 7, n), 18, 60).round(1)
    purchase_count = np.clip(rng.normal(3.1, 1.7, n), 1, 9).astype(int)
    recency_days = np.clip(rng.normal(55, 25, n), 3, 180).astype(int)
    coupon_sensitivity = rng.choice(["高", "中", "低"], size=n, p=[0.35, 0.45, 0.2])
    pred_ite = np.round(rng.normal(0.08, 0.04, n), 4)
    pred_ite[uplift_type == "反作用型"] = np.round(rng.normal(-0.02, 0.01, (uplift_type == "反作用型").sum()), 4)
    df = pd.DataFrame({
        "user_id": user_ids,
        "gender": gender,
        "province": province,
        "skin_type": skin_type,
        "member_status": member,
        "age": age,
        "purchase_count": purchase_count,
        "recency_days": recency_days,
        "uplift_type": uplift_type,
        "coupon_sensitivity": coupon_sensitivity,
        "pred_ite": pred_ite,
    })
    return enrich_user_profile(df)

@st.cache_data
def load_real_data():
    def read_csv_auto(path, nrows=None):
        for enc in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
            try:
                return pd.read_csv(path, encoding=enc, nrows=nrows)
            except Exception:
                continue
        # 最后兜底，避免个别文件编码异常导致整页不可用
        return pd.read_csv(path, nrows=nrows)

    root = Path(__file__).resolve().parent
    search_roots = [
        root,
        root / "data",
        root / "data" / "数据集",
    ]

    user_path = None
    order_path = None
    cluster_files = []
    for sr in search_roots:
        if not sr.exists():
            continue
        if user_path is None:
            cand = list(sr.rglob("珀莱雅用户数据_最终版.csv"))
            if cand:
                user_path = cand[0]
        if order_path is None:
            cand = list(sr.rglob("珀莱雅订单数据_最终版.csv"))
            if cand:
                order_path = cand[0]
        cluster_files.extend(sr.rglob("簇*.csv"))
    cluster_files = list(dict.fromkeys(cluster_files))

    # 优先使用固定文件名；若不存在，则自动按列名识别 CSV 角色
    if user_path is None or order_path is None:
        auto_user_path = None
        auto_order_path = None
        auto_cluster_files = []
        csv_candidates = []
        for sr in search_roots:
            if sr.exists():
                csv_candidates.extend(sr.rglob("*.csv"))
        for f in csv_candidates:
            try:
                preview = read_csv_auto(f, nrows=5)
            except Exception:
                continue
            cols = set(preview.columns.astype(str))
            # 用户表特征
            if {"用户ID", "年龄", "肤质"}.issubset(cols) or {"user_id", "age", "skin_type"}.issubset(cols):
                if auto_user_path is None:
                    auto_user_path = f
                continue
            # 订单表特征
            if {"订单ID", "用户ID"}.issubset(cols) or {"order_id", "user_id"}.issubset(cols):
                if auto_order_path is None:
                    auto_order_path = f
                continue
            # 簇/分群文件特征
            if "cluster_name" in cols or "簇" in f.stem:
                auto_cluster_files.append(f)
        if auto_user_path is not None:
            user_path = auto_user_path
        if auto_order_path is not None:
            order_path = auto_order_path
        if auto_cluster_files:
            cluster_files = auto_cluster_files

    if user_path is None or order_path is None or (not user_path.exists()) or (not order_path.exists()):
        return None, None, False

    users_raw = read_csv_auto(user_path)
    orders = read_csv_auto(order_path)
    users_df = users_raw.rename(columns={
        "用户ID": "user_id",
        "性别": "gender",
        "年龄": "age",
        "肤质": "skin_type",
        "是否会员": "member_status",
        "常用省份": "province",
    }).copy()
    orders = orders.rename(columns={
        "订单ID": "order_id",
        "用户ID": "user_id",
        "下单时间": "order_time",
        "商品大类": "category",
        "商品子类": "sub_category",
        "商品名称": "product_name",
        "单价": "unit_price",
        "购买数量": "quantity",
        "订单总额": "order_amount",
    }).copy()

    # 兼容缺失列：保证后续计算不中断
    for col, default_value in {
        "user_id": "",
        "gender": "女",
        "age": 30,
        "skin_type": "中性",
        "member_status": "否",
        "province": "未知",
    }.items():
        if col not in users_df.columns:
            users_df[col] = default_value

    for col, default_value in {
        "order_id": np.arange(len(orders)),
        "user_id": "",
        "order_time": pd.Timestamp.today().strftime("%Y-%m-%d"),
        "category": "护肤",
        "sub_category": "其他",
        "product_name": "未命名商品",
        "unit_price": 0.0,
        "quantity": 1,
        "order_amount": np.nan,
    }.items():
        if col not in orders.columns:
            orders[col] = default_value

    if orders["order_amount"].isna().any():
        orders["order_amount"] = orders["order_amount"].fillna(
            pd.to_numeric(orders["unit_price"], errors="coerce").fillna(0.0)
            * pd.to_numeric(orders["quantity"], errors="coerce").fillna(1.0)
        )

    orders["order_time"] = pd.to_datetime(orders["order_time"], errors="coerce")
    orders["series"] = orders["product_name"].apply(detect_series)
    order_level = orders.groupby(["user_id", "order_id", "order_time"], as_index=False).agg(order_amount=("order_amount", "sum"))
    ref_date = order_level["order_time"].max() + pd.Timedelta(days=1)
    user_orders = order_level.groupby("user_id", as_index=False).agg(
        purchase_count=("order_id", "nunique"),
        total_spend=("order_amount", "sum"),
        avg_order_value=("order_amount", "mean"),
        last_order_time=("order_time", "max"),
    )
    user_orders["recency_days"] = (ref_date - user_orders["last_order_time"]).dt.days
    series_pref = orders.groupby(["user_id", "series"], as_index=False).agg(amount=("order_amount", "sum"))
    series_pref = series_pref.sort_values(["user_id", "amount"], ascending=[True, False])
    top_series = series_pref.groupby("user_id").head(2).copy()
    top_series["rank"] = top_series.groupby("user_id").cumcount() + 1
    top1 = top_series[top_series["rank"] == 1][["user_id", "series"]].rename(columns={"series": "top_series"})
    top2 = top_series[top_series["rank"] == 2][["user_id", "series"]].rename(columns={"series": "second_series"})
    cluster_df = pd.DataFrame(columns=["user_id", "cluster_name"])
    if cluster_files:
        cluster_list = []
        for f in cluster_files:
            c = read_csv_auto(f)
            c = c.rename(columns={"用户ID": "user_id"})
            cluster_list.append(c[["user_id", "cluster_name"]])
        cluster_df = pd.concat(cluster_list, ignore_index=True).drop_duplicates(subset=["user_id"])
    df = users_df.merge(user_orders, on="user_id", how="left")
    df = df.merge(top1, on="user_id", how="left")
    df = df.merge(top2, on="user_id", how="left")
    if not cluster_df.empty:
        df = df.merge(cluster_df, on="user_id", how="left")
    else:
        df["cluster_name"] = np.nan
    df["purchase_count"] = df["purchase_count"].fillna(0).astype(int)
    df["total_spend"] = df["total_spend"].fillna(0.0)
    df["avg_order_value"] = df["avg_order_value"].fillna(0.0)
    df["recency_days"] = df["recency_days"].fillna(999).astype(int)
    df["top_series"] = df["top_series"].fillna("基础保湿系列")
    df["second_series"] = df["second_series"].fillna("双抗系列")
    return enrich_user_profile(df), orders, True

def enrich_user_profile(df):
    df = df.copy()
    # 兜底补齐字段：避免不同数据源下出现 KeyError
    default_columns = {
        "top_series": "基础保湿系列",
        "second_series": "双抗系列",
        "total_spend": 0.0,
        "avg_order_value": 0.0,
        "cluster_name": np.nan,
    }
    for col, default_value in default_columns.items():
        if col not in df.columns:
            df[col] = default_value
    # 若存在缺失值，统一补齐默认值
    df["top_series"] = df["top_series"].fillna("基础保湿系列")
    df["second_series"] = df["second_series"].fillna("双抗系列")
    df["total_spend"] = pd.to_numeric(df["total_spend"], errors="coerce").fillna(0.0)
    df["avg_order_value"] = pd.to_numeric(df["avg_order_value"], errors="coerce").fillna(0.0)

    def parse_cluster_value(x):
        text = str(x) if pd.notna(x) else ""
        if "高价值" in text:
            return "核心价值用户"
        if "中价值" in text:
            return "潜力发展用户"
        if "低价值" in text:
            return "低价值/流失用户"
        return None
    df["rfm_from_cluster"] = df.get("cluster_name", pd.Series(index=df.index, dtype=object)).apply(parse_cluster_value)
    def rfm_rule(row):
        if pd.notna(row["rfm_from_cluster"]):
            return row["rfm_from_cluster"]
        if row["purchase_count"] >= 4 and row["recency_days"] <= 60:
            return "核心价值用户"
        if row["purchase_count"] >= 2 and row["recency_days"] <= 120:
            return "潜力发展用户"
        if row["purchase_count"] >= 1 and row["recency_days"] <= 240:
            return "高价值沉睡用户"
        return "低价值/流失用户"
    df["rfm_segment"] = df.apply(rfm_rule, axis=1)
    def parse_kmeans(x, skin):
        text = str(x) if pd.notna(x) else ""
        if "_" in text:
            parts = text.split("_")
            if len(parts) >= 3:
                return parts[2]
        mapping = {
            "敏感肌": "修护+保湿",
            "油性/混油": "清爽+抗氧化",
            "干性/混干": "抗皱+抗衰",
            "中性": "抗氧化+保湿",
        }
        return mapping.get(skin, "全能功效")
    df["kmeans_cluster"] = [parse_kmeans(c, s) for c, s in zip(df.get("cluster_name", pd.Series(index=df.index)), df["skin_type"])]
    def baseline_prob(row):
        if row["purchase_count"] >= 5:
            base = 0.45
        elif row["purchase_count"] >= 3:
            base = 0.35
        elif row["purchase_count"] >= 1:
            base = 0.20
        else:
            base = 0.08
        if row["member_status"] in ["是", "会员"]:
            base += 0.08
        if row["recency_days"] <= 30:
            base += 0.12
        return min(base, 0.65)
    def uplift_score(row):
        uplift = 0.0
        is_member = row["member_status"] in ["是", "会员"]
        if is_member:
            if row["purchase_count"] >= 5:
                uplift += 0.15
            elif row["purchase_count"] >= 2:
                uplift += 0.12
            else:
                uplift += 0.08
        else:
            if row["purchase_count"] >= 3:
                uplift += 0.10
            elif row["purchase_count"] >= 1:
                uplift += 0.06
            else:
                uplift += 0.04
        if 25 <= row["age"] <= 35:
            uplift += 0.03
        if row["skin_type"] in ["混合性", "油性", "油性/混油"]:
            uplift += 0.02
        if row["recency_days"] <= 15:
            uplift -= 0.02
        return float(np.clip(uplift, -0.05, 0.25))
    df["baseline_prob"] = df.apply(baseline_prob, axis=1)
    df["pred_ite"] = df.apply(uplift_score, axis=1).round(4)
    p70 = float(np.percentile(df["pred_ite"], 70)) if len(df) else 0.08
    p10 = float(np.percentile(df["pred_ite"], 10)) if len(df) else -0.01
    def uplift_rule(row):
        ite = row["pred_ite"]
        if ite > p70:
            return "敏感型"
        elif ite > 0:
            return "自然转化型"
        elif ite > p10:
            return "无兴趣型"
        return "反作用型"
    df["uplift_type"] = df.apply(uplift_rule, axis=1)
    def coupon_rule(row):
        if row["uplift_type"] == "敏感型" and row["member_status"] in ["否", "非会员"]:
            return "高"
        if row["uplift_type"] == "反作用型":
            return "低"
        return "中"
    df["coupon_sensitivity"] = df.apply(coupon_rule, axis=1)
    def priority(row):
        if row["uplift_type"] == "敏感型" and row["rfm_segment"] in ["核心价值用户", "潜力发展用户"]:
            return "A-重点触达"
        if row["uplift_type"] == "自然转化型":
            return "B-内容种草"
        if row["rfm_segment"] == "高价值沉睡用户":
            return "B-召回测试"
        return "C-低频维护"
    df["touch_priority"] = df.apply(priority, axis=1)
    df["member_status"] = df["member_status"].replace({"会员": "是", "非会员": "否"})
    return df

@st.cache_data
def build_trend_from_orders(orders):
    if orders is None or orders.empty:
        return pd.DataFrame({"month": [], "sales_wan": [], "active_users": []})
    df = orders.copy()
    df["month"] = df["order_time"].dt.to_period("M").dt.to_timestamp()
    trend = df.groupby("month", as_index=False).agg(
        sales=("order_amount", "sum"),
        active_users=("user_id", pd.Series.nunique),
    )
    trend["sales_wan"] = trend["sales"] / 10000
    return trend

@st.cache_data
def build_series_sales_from_orders(orders):
    if orders is None or orders.empty:
        return pd.DataFrame({"series": [], "sales": [], "share": []})
    s = orders.groupby("series", as_index=False).agg(sales=("order_amount", "sum"))
    s = s.sort_values("sales", ascending=False)
    s["share"] = s["sales"] / s["sales"].sum() * 100
    return s.head(8)

users_real, orders_real, real_loaded = load_real_data()
require_real_data = os.getenv("REQUIRE_REAL_DATA", "1").lower() in {"1", "true", "yes", "y"}
if real_loaded:
    users = users_real
    orders = orders_real
    data_status = "真实数据模式"
else:
    if require_real_data:
        st.error("未读取到真实数据文件，已阻止进入演示数据模式。请检查 data/数据集 下的 CSV 是否完整。")
        st.stop()
    users = build_demo_data()
    orders = None
    data_status = "演示数据模式"

trend_df = build_trend_from_orders(orders)
series_df = build_series_sales_from_orders(orders)
if series_df.empty:
    series_df = pd.DataFrame({
        "series": ["双抗系列", "红宝石系列", "源力系列", "基础保湿系列", "能量系列"],
        "sales": [66960862, 50303862, 36482909, 10567061, 4252458],
        "share": [39.7, 29.8, 21.6, 6.3, 2.5],
    })

qini_df = pd.DataFrame({
    "x": np.linspace(0, 1, 21),
    "baseline": np.linspace(0, 100, 21),
    "model": [0, 8, 15, 23, 31, 36, 42, 48, 55, 61, 67, 73, 79, 84, 89, 93, 96, 98, 99, 100, 100],
})

def strategy_engine(row):
    uplift_type = row["uplift_type"]
    skin = row["skin_type"]
    series = row["top_series"]
    coupon = row["coupon_sensitivity"]
    if uplift_type == "敏感型":
        touch = "建议触达"
        tone = "温和关怀 + 轻促销"
        frequency = "每月 1-2 次"
        coupon_plan = "满200减30 / 满300减50"
    elif uplift_type == "自然转化型":
        touch = "谨慎发券，内容种草优先"
        tone = "专业推荐 + 会员权益"
        frequency = "每季度 1 次"
        coupon_plan = "弱化优惠，突出新品/功效"
    elif uplift_type == "无兴趣型":
        touch = "低频试探触达"
        tone = "轻提醒 + 低打扰"
        frequency = "每季度 1 次或更低"
        coupon_plan = "小额福利测试"
    else:
        touch = "不建议营销打扰"
        tone = "服务提醒 / 品牌关怀"
        frequency = "原则上不触达"
        coupon_plan = "不发券"
    skin_reason = {
        "敏感肌": "突出修护、舒缓、屏障稳定",
        "油性/混油": "强调清爽、抗氧、肤感轻盈",
        "干性/混干": "强调保湿、滋润、抗皱抗老",
        "中性": "强调维稳、提亮、抗初老",
    }.get(skin, "强调功效匹配与肤质适配")
    if coupon == "高" and uplift_type == "敏感型":
        comm = "可在文案中突出限时专属福利与到期提醒，促进即时转化。"
    elif coupon == "低":
        comm = "不建议过度强调价格，更适合讲功效、成分和长期护肤价值。"
    else:
        comm = "建议平衡福利表达与产品功效表达，保持品牌质感。"
    return {
        "touch": touch,
        "tone": tone,
        "frequency": frequency,
        "coupon_plan": coupon_plan,
        "focus": skin_reason,
        "comment": comm,
        "series": series,
    }

def generate_message(row, style="温柔关怀版"):
    skin = row["skin_type"]
    series = row["top_series"]
    second = row.get("second_series", "基础保湿系列")
    coupon = row["coupon_sensitivity"]
    uplift_type = row["uplift_type"]
    pain_map = {
        "敏感肌": ("换季泛红、屏障不稳", "修护舒缓"),
        "油性/混油": ("出油暗沉、肤感负担", "清爽抗氧"),
        "干性/混干": ("干燥细纹、紧绷缺水", "滋润抗老"),
        "中性": ("肤况波动、初老提亮", "维稳提亮"),
    }
    pain, benefit = pain_map.get(skin, ("肌肤状态波动", "综合护理"))
    if uplift_type == "反作用型":
        return f"亲爱的用户，近期为减少打扰，我们为你保留了更简洁的护肤服务提醒。若你近期关注 {benefit} 方向，可优先了解 {series}，也可搭配 {second} 作为日常护理补充。"
    if uplift_type == "无兴趣型":
        return f"Hi，这次给你准备了一条更轻量的护肤建议：如果你最近关注 {benefit}，可以先从 {series} 开始了解，搭配 {second} 会更完整。我们尽量减少打扰，只在真正适合你的时候再推荐。"
    coupon_part = "本次可领取专属福利，适合趁机入手。" if coupon == "高" else "这次也为你准备了轻量福利。" if coupon == "中" else "这次更想把适合你的护理方案推荐给你。"
    if style == "温柔关怀版":
        return f"Hi，最近天气变化大，像你这类 {skin} 用户更容易出现 {pain}。我们更推荐你关注 {series}，更贴合当下的 {benefit} 需求，搭配 {second} 使用会更完整。{coupon_part}"
    if style == "促销转化版":
        return f"适合 {skin} 的 {series} 现在是重点推荐系列，针对 {pain} 更有针对性。现在入手再搭配 {second}，更适合做一整套护理方案。{coupon_part}"
    return f"结合你的肤质与近期偏好，我们为你优先匹配了 {series}。它更适合解决 {pain} 问题，同时建议搭配 {second} 完善日常护理。本次推荐以 {benefit} 为核心方向。"

# ===================== 顶部标题 =====================
st.markdown("""
<div class="hero-box">
    <h1>解码“她”的数据：精准营销策略生成系统</h1>
</div>
""", unsafe_allow_html=True)

# ===================== 8个页面按钮 =====================
btn_list = [
    "首页总览",
    "用户洞察中心",
    "肤质与产品匹配",
    "Uplift决策中心",
    "关联规则洞察",
    "ROI策略模拟",
    "智能私信助手",
    "目标名单导出"
]

if "page" not in st.session_state:
    st.session_state.page = "首页总览"

cols = st.columns(8)
for i, name in enumerate(btn_list):
    with cols[i]:
        if st.button(name, use_container_width=True):
            st.session_state.page = name

# ===================== 筛选器 默认隐藏 =====================
with st.expander("高级筛选", expanded=False):
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        uplift_options = sorted(users["uplift_type"].unique())
        selected_uplift = st.selectbox("Uplift 类型", ["全部"] + uplift_options, index=0)
    with c2:
        rfm_options = sorted(users["rfm_segment"].unique())
        selected_rfm = st.selectbox("RFM 分层", ["全部"] + rfm_options, index=0)
    with c3:
        skin_options = sorted(users["skin_type"].dropna().unique())
        selected_skin = st.selectbox("肤质类型", ["全部"] + skin_options, index=0)
    with c4:
        coupon_options = sorted(users["coupon_sensitivity"].unique())
        selected_coupon = st.selectbox("优惠敏感度", ["全部"] + coupon_options, index=0)
    with c5:
        st.markdown('<div class="filter-label">用户年龄</div>', unsafe_allow_html=True)
        min_age = int(max(18, users["age"].fillna(18).min()))
        max_age = int(min(60, users["age"].fillna(60).max()))
        age_range = st.slider("年龄", min_age, max_age, (min_age, max_age), label_visibility="collapsed")

filtered = users[
    (users["uplift_type"].eq(selected_uplift) if selected_uplift != "全部" else True) &
    (users["rfm_segment"].eq(selected_rfm) if selected_rfm != "全部" else True) &
    (users["skin_type"].eq(selected_skin) if selected_skin != "全部" else True) &
    (users["coupon_sensitivity"].eq(selected_coupon) if selected_coupon != "全部" else True) &
    users["age"].between(age_range[0], age_range[1])
].copy()

st.markdown(f"当前筛选用户：**{len(filtered):,}** ｜ 数据状态：**{data_status}**")
st.markdown("---")

# ===================== 页面内容 =====================
page = st.session_state.page

if page == "首页总览":
    total_orders = 0 if orders is None else orders["order_id"].nunique()
    total_sales = 0 if orders is None else orders.groupby("order_id")["order_amount"].sum().sum()
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("用户总量", f"{len(users):,}", "系统已接入用户主表")
    with c2: metric_card("订单总量", f"{total_orders:,}", "按订单ID统计")
    with c3: metric_card("总销售额", f"{total_sales/10000:,.1f} 万", "按订单明细汇总")
    with c4: metric_card("敏感型用户占比", f"{(users['uplift_type'].eq('敏感型').mean()*100):.1f}%", "适合重点营销触达")
    st.markdown("<div class='section-tip'>现在首页的指标和图表会优先基于你上传的真实 CSV 自动生成。</div>", unsafe_allow_html=True)
    left, right = st.columns([1.05, 0.95])
    with left:
        dist = filtered.groupby(["rfm_segment", "uplift_type"]).size().reset_index(name="count")
        fig = px.sunburst(dist, path=["rfm_segment", "uplift_type"], values="count", color="rfm_segment", color_discrete_map=PALETTE)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"), margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(series_df, x="series", y="sales", color="series", text="share", color_discrete_map=PALETTE)
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="", yaxis_title="销售额", font=dict(color="#eef7ff"), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    if not trend_df.empty:
        left2, right2 = st.columns([1.05, 0.95])
        with left2:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=trend_df["month"], y=trend_df["sales_wan"], mode="lines+markers", name="销售额（万元）", line=dict(color="#57c7ff", width=3)), secondary_y=False)
            fig.add_trace(go.Scatter(x=trend_df["month"], y=trend_df["active_users"], mode="lines+markers", name="活跃用户", line=dict(color="#7de3d6", width=3)), secondary_y=True)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"), legend=dict(orientation="h", y=1.06))
            st.plotly_chart(fig, use_container_width=True)
        with right2:
            top_skin = filtered["skin_type"].mode().iloc[0] if len(filtered) else users["skin_type"].mode().iloc[0]
            top_series = filtered["top_series"].mode().iloc[0] if len(filtered) else users["top_series"].mode().iloc[0]
            st.markdown(f"""<div class="glass-card"><p><b>当前人群画像总结</b></p><p>当前筛选人群以 <b>{top_skin}</b> 为主，推荐聚焦 <b>{top_series}</b> 相关系列。</p></div>""", unsafe_allow_html=True)

elif page == "用户洞察中心":
    st.markdown("### 用户洞察中心")
    c1, c2 = st.columns(2)
    with c1:
        gender_df = filtered["gender"].value_counts().reset_index()
        gender_df.columns = ["gender", "count"]
        fig = px.pie(gender_df, names="gender", values="count", hole=0.62, color_discrete_sequence=["#57c7ff", "#7de3d6"])
        fig.update_layout(title="性别分布", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        province_df = filtered["province"].value_counts().reset_index().head(10)
        province_df.columns = ["province", "count"]
        fig = px.bar(province_df, x="province", y="count", color="count", color_continuous_scale=["#123865", "#57c7ff", "#7de3d6"])
        fig.update_layout(title="Top地区分布", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
        st.plotly_chart(fig, use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        rfm_df = filtered["rfm_segment"].value_counts().reset_index()
        rfm_df.columns = ["segment", "count"]
        fig = px.bar(rfm_df, x="segment", y="count", color="segment", color_discrete_map=PALETTE)
        fig.update_layout(title="RFM 用户价值分层", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        cluster_df = filtered["kmeans_cluster"].value_counts().reset_index()
        cluster_df.columns = ["cluster", "count"]
        fig = px.treemap(cluster_df, path=["cluster"], values="count", color="count", color_continuous_scale=["#123865", "#57c7ff", "#d6b7ff"])
        fig.update_layout(title="功效偏好聚类", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"), margin=dict(t=40, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered[["user_id", "age", "skin_type", "province", "rfm_segment", "kmeans_cluster", "top_series"]].head(30), use_container_width=True, hide_index=True)

elif page == "肤质与产品匹配":
    st.markdown("### 肤质与产品匹配")
    matrix = pd.DataFrame(SKIN_SERIES_PREFERENCE).T[["源力系列", "红宝石系列", "双抗系列", "能量系列", "基础保湿系列"]]
    fig = px.imshow(matrix, text_auto=True, aspect="auto", color_continuous_scale=["#102b4b", "#2a5d9f", "#57c7ff", "#7de3d6"])
    fig.update_layout(title="肤质-产品系列匹配度矩阵", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
    st.plotly_chart(fig, use_container_width=True)
    left, right = st.columns([1, 1])
    with left:
        skin_input = st.selectbox("选择肤质", sorted(users["skin_type"].dropna().unique()))
        concern_input = st.selectbox("选择皮肤问题", ["敏感泛红", "细纹皱纹", "暗沉发黄", "松弛下垂", "干燥缺水", "综合护理"])
        base_scores = matrix.loc[skin_input].to_dict() if skin_input in matrix.index else {k: 0.5 for k in matrix.columns}
        final_scores = base_scores.copy()
        for k, v in CONCERN_BOOST.get(concern_input, {}).items():
            if k in final_scores:
                final_scores[k] = min(1.0, final_scores[k] + v)
        rec_df = pd.DataFrame({"series": list(final_scores.keys()), "score": list(final_scores.values())}).sort_values("score", ascending=False)
        fig2 = px.bar(rec_df, x="series", y="score", color="series", color_discrete_map=PALETTE)
        fig2.update_layout(title="个性化推荐得分", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    with right:
        top3 = rec_df.head(3)["series"].tolist()
        st.markdown(f"""<div class="glass-card"><p><b>推荐结果</b></p><p>肤质：<b>{skin_input}</b>｜问题：<b>{concern_input}</b></p><p>Top1：{top3[0]}｜Top2：{top3[1]}｜Top3：{top3[2]}</p></div>""", unsafe_allow_html=True)
        fig3 = px.pie(series_df, names="series", values="sales", hole=0.55, color="series", color_discrete_map=PALETTE)
        fig3.update_layout(title="系列销售结构", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
        st.plotly_chart(fig3, use_container_width=True)

elif page == "Uplift决策中心":
    st.markdown("### Uplift 决策中心")
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("敏感型人数", f"{users['uplift_type'].eq('敏感型').sum():,}", "高优先级触达")
    with c2: metric_card("自然转化型", f"{users['uplift_type'].eq('自然转化型').sum():,}", "内容种草")
    with c3: metric_card("反作用型", f"{users['uplift_type'].eq('反作用型').sum():,}", "避免打扰")
    with c4: metric_card("平均ITE", f"{users['pred_ite'].mean():.3f}", "营销增益")
    left, right = st.columns(2)
    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qini_df["x"], y=qini_df["model"], mode="lines+markers", name="Uplift 模型", line=dict(color="#57c7ff", width=4)))
        fig.add_trace(go.Scatter(x=qini_df["x"], y=qini_df["baseline"], mode="lines", name="随机基线", line=dict(color="#7de3d6", dash="dash")))
        fig.update_layout(title="Qini 曲线", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        cat_df = filtered["uplift_type"].value_counts().reset_index()
        cat_df.columns = ["类别", "人数"]
        fig = px.funnel_area(cat_df, names="类别", values="人数", color="类别", color_discrete_map=PALETTE)
        fig.update_layout(title="当前筛选人群 ITE 分类", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
        st.plotly_chart(fig, use_container_width=True)
    compare_df = users.groupby("uplift_type", as_index=False).agg(avg_age=("age", "mean"), avg_purchase=("purchase_count", "mean"), avg_recency=("recency_days", "mean"), avg_spend=("total_spend", "mean"))
    st.dataframe(compare_df.round(2), use_container_width=True, hide_index=True)

elif page == "关联规则洞察":
    st.markdown("### 关联规则洞察")
    if orders is not None and not orders.empty and "sub_category" in orders.columns:
        basket = pd.crosstab(orders["order_id"], orders["sub_category"])
        if basket.shape[1] >= 2:
            sim = basket.corr().fillna(0)
            fig = px.imshow(sim, text_auto=True, aspect="auto", color_continuous_scale=["#102b4b", "#2a5d9f", "#57c7ff", "#7de3d6"])
            fig.update_layout(title="商品相关性", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
            st.plotly_chart(fig, use_container_width=True)
            support_rows = []
            binary = (basket > 0).astype(int)
            cols = binary.columns.tolist()
            for a in cols:
                for b in cols:
                    if a == b: continue
                    support = ((binary[a] == 1) & (binary[b] == 1)).mean()
                    conf = ((binary[a] == 1) & (binary[b] == 1)).sum() / max((binary[a] == 1).sum(), 1)
                    base_b = (binary[b] == 1).mean()
                    lift = conf / base_b if base_b > 0 else 0
                    support_rows.append([a, b, support, conf, lift])
            rules_df = pd.DataFrame(support_rows, columns=["前提", "结论", "支持度", "置信度", "提升度"])
            rules_df = rules_df[(rules_df["支持度"] >= 0.01) & (rules_df["提升度"] > 1)].sort_values(["置信度", "提升度"], ascending=False).head(20)
            st.dataframe(rules_df.round(3), use_container_width=True, hide_index=True)
        else:
            st.info("商品类型不足，无法生成规则")
    else:
        st.info("订单数据不足")

elif page == "ROI策略模拟":
    st.markdown("### ROI策略模拟")
    col1, col2, col3 = st.columns(3)
    profit = col1.number_input("单利润", 10.0, 300.0, 75.0, 5.0)
    coupon_cost = col2.number_input("优惠券成本", 1.0, 50.0, 4.5, 0.5)
    send_ratio = col3.slider("触达比例", 0.05, 1.0, 0.35)
    ranked = filtered.sort_values("pred_ite", ascending=False)
    top_n = max(1, int(len(ranked)*send_ratio))
    target = ranked.head(top_n)
    target["expected_net"] = target["pred_ite"]*profit - coupon_cost
    total_net = target["expected_net"].sum()
    random_net = (filtered["pred_ite"].mean()*profit - coupon_cost)*top_n if len(filtered) else 0
    improve = ((total_net-random_net)/abs(random_net)*100) if random_net !=0 else 0
    k1,k2,k3,k4 = st.columns(4)
    with k1: metric_card("建议发送", f"{top_n}", "按ITE排序")
    with k2: metric_card("预期净收益", f"{total_net:.0f}", "元")
    with k3: metric_card("随机收益", f"{random_net:.0f}", "元")
    with k4: metric_card("提升", f"{improve:.1f}%", "")
    curve = ranked.copy()
    curve["expected_net"] = curve["pred_ite"]*profit - coupon_cost
    curve["cum_net"] = curve["expected_net"].cumsum()
    curve["ratio"] = np.arange(1, len(curve)+1)/len(curve) if len(curve) else []
    if len(curve):
        fig = px.line(curve, x="ratio", y="cum_net")
        fig.add_vline(x=send_ratio, line_dash="dash", line_color="#7de3d6")
        fig.update_traces(line_color="#57c7ff")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eef7ff"))
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(target[["user_id","uplift_type","rfm_segment","skin_type","top_series","coupon_sensitivity","pred_ite"]].head(30), use_container_width=True, hide_index=True)

elif page == "智能私信助手":
    st.markdown("### 智能私信助手")
    mode = st.radio("模式", ["单用户模式", "人群策略模式"], horizontal=True)
    if mode == "单用户模式":
        user_list = filtered["user_id"].head(500).tolist() if len(filtered) else users["user_id"].head(500).tolist()
        user_pick = st.selectbox("选择用户", user_list)
        row = users[users["user_id"] == user_pick].iloc[0]
        strategy = strategy_engine(row)
        left, right = st.columns(2)
        with left:
            up = pd.DataFrame({"字段":["用户ID","年龄","肤质","RFM","Uplift","推荐系列","优惠敏感度","ITE"],
                               "内容":[row["user_id"],row["age"],row["skin_type"],row["rfm_segment"],row["uplift_type"],row["top_series"],row["coupon_sensitivity"],row["pred_ite"]]})
            st.dataframe(up, use_container_width=True, hide_index=True)
        with right:
            st.markdown(f"""<div class="glass-card">
            <p>触达：{strategy['touch']}</p>
            <p>系列：{strategy['series']}</p>
            <p>语气：{strategy['tone']}</p>
            <p>优惠：{strategy['coupon_plan']}</p>
            <p>频次：{strategy['frequency']}</p>
            <p>重点：{strategy['focus']}</p></div>""", unsafe_allow_html=True)
        style = st.selectbox("文案风格", ["温柔关怀版","促销转化版","会员尊享版"])
        st.code(generate_message(row, style))
    else:
        c1,c2,c3,c4 = st.columns(4)
        up = c1.selectbox("Uplift", sorted(users["uplift_type"].unique()))
        rp = c2.selectbox("RFM", sorted(users["rfm_segment"].unique()))
        sp = c3.selectbox("肤质", sorted(users["skin_type"].dropna().unique()))
        cp = c4.selectbox("优惠敏感度", sorted(users["coupon_sensitivity"].unique()))
        seg = users[(users["uplift_type"]==up)&(users["rfm_segment"]==rp)&(users["skin_type"]==sp)&(users["coupon_sensitivity"]==cp)]
        st.markdown(f"匹配人群：**{len(seg)}**")
        if len(seg):
            row = seg.iloc[0]
            st.code(generate_message(row, "温柔关怀版"))
            st.code(generate_message(row, "促销转化版"))
            st.code(generate_message(row, "会员尊享版"))

elif page == "目标名单导出":
    st.markdown("### 目标名单导出")
    em = st.selectbox("导出模式", ["敏感型用户名单","ROI最优名单","当前筛选名单","按簇导出名单","无兴趣型试探名单"])
    if em == "敏感型用户名单":
        ed = users[users["uplift_type"]=="敏感型"].sort_values("pred_ite", ascending=False)
    elif em == "ROI最优名单":
        ed = users.sort_values("pred_ite", ascending=False).head(int(len(users)*0.35))
    elif em == "无兴趣型试探名单":
        ed = users[users["uplift_type"]=="无兴趣型"]
    elif em == "按簇导出名单":
        cls = sorted(users["cluster_name"].dropna().unique())
        if cls:
            cp = st.selectbox("选择簇", cls)
            ed = users[users["cluster_name"]==cp]
        else:
            ed = users.head(0)
    else:
        ed = filtered.copy()
    if len(ed):
        show_cols = ["user_id","age","province","skin_type","member_status","rfm_segment","uplift_type","coupon_sensitivity","pred_ite","top_series"]
        show_cols = [c for c in show_cols if c in ed.columns]
        st.dataframe(ed[show_cols].head(100), use_container_width=True, hide_index=True)
        csv = ed[show_cols].to_csv(index=False).encode("utf-8-sig")
        st.download_button("CSV导出", csv, f"名单_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", use_container_width=True)

st.markdown("---")
