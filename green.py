import streamlit as st

st.set_page_config(page_title="臺北市建築綠化計算器", layout="wide")

st.title("🌿 臺北市新建建築物綠化實施規則 (2026新制) 計算器")
st.caption("整合「綠覆率」與「等效綠容率 (GVR)」自動檢核系統")

# --- 側邊欄：基地基本資料 ---
st.sidebar.header("📍 第一步：輸入基地資料")
area_base = st.sidebar.number_input("建築基地面積 (㎡)", min_value=1.0, value=1000.0)
area_open = st.sidebar.number_input("法定空地面積 (㎡)", min_value=1.0, value=400.0)
zone_type = st.sidebar.selectbox("基地類別 (依規則第4條)", [1, 2, 3, 4, 5], index=0)

# 自動判定標準 (GVR 標準)
gvr_standards = {1: 2.0, 2: 1.9, 3: 1.8, 4: 1.6, 5: 1.4}
ratio_standards ={1: 0.9, 2: 0.8, 3: 0.7, 4: 0.6, 5:0.5}
target_gvr = gvr_standards[zone_type]
target_ratio = ratio_standards[zone_type]

# --- 主畫面：植栽輸入區 ---
st.header("🌳 第二步：輸入植栽配置")
col1, col2, col3 = st.columns(3)

with col1:
    tree_high = st.number_input("高遮蔭喬木 (株)", min_value=0, value=10)
    tree_low = st.number_input("低遮蔭喬木 (株)", min_value=0, value=5)
with col2:
    shrub_area = st.number_input("灌木面積 (㎡)", min_value=0.0, value=50.0)
    grass_area = st.number_input("地被草皮面積 (㎡)", min_value=0.0, value=100.0)
with col3:
    wall_area = st.number_input("立面綠化面積 (㎡)", min_value=0.0, value=30.0)
    is_near_road = st.checkbox("立面綠化是否鄰接道路 (加成 5%)")

# --- 核心邏輯計算 ---
# 1. 綠覆面積 Ag (現行指標)
ag_total = (tree_high * 16) + (tree_low * 12) + shrub_area + grass_area + wall_area
current_ratio = ag_total / area_open

# 2. 等效綠覆 Ae (2026 GVR 指標)
fc_wall = 1.575 if is_near_road else 1.5
ae_total = (tree_high * 16 * 3.0) + (tree_low * 12 * 2.0) + (shrub_area * 1.2) + (grass_area * 1.0) + (wall_area * fc_wall)
current_gvr = ae_total / area_base

# --- 第三步：結果呈現 ---
st.divider()
st.header("📊 第三步：法規檢核結果")

res1, res2 = st.columns(2)

with res1:
    st.metric("現行綠覆率", f"{current_ratio:.2%}")
    if current_ratio >= target_ratio:
        st.success(f"✅ 綠覆率符合{zone_type} 類降溫標準 (>= {target_ratio})")
    else:
        st.error(f"❌ 綠覆率不足 (標準: {target_ratio})")

with res2:
    st.metric("2026 新制綠容率 (GVR)", f"{current_gvr:.2f}")
    if current_gvr >= target_gvr:
        st.success(f"✅ 符合第 {zone_type} 類降溫標準 (>= {target_gvr})")
    else:
        st.error(f"❌ 綠容率不足 (標準: {target_gvr})")

st.info(f"💡 註：本計算參考 2026 年臺北市降溫城市新制，高遮蔭喬木權重 3.0，低遮蔭 2.0。")
