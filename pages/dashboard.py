import os
import streamlit as st
import streamlit_app as app
import pandas as pd
import numpy as np
from modules.libbase import load_firebase
import modules.builddata as builddata
from modules import pretime
load_firebase()
import time
app.sidebar_menu()
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import datetime
from data_demo.metric import history
components.html(
"""
    <script>
        window.addEventListener( 'resize', () => {
            window.parent.postMessage("triggerResize", "*");
        });
    </script>
""", height=0
)

metrics = [
    {
        "title": "Cân nặng (kg)",
        "id": "weight",
        "unit": "kg",
        "note": None,
        "target": None,
    },
    {
        "title": "Chiều cao (cm)",
        "id": "height",
        "unit": "cm",
        "note": None,
        "target": None,
    },
    {
        "title": "Calo nạp (kcal)",
        "id": "kcal",
        "unit": "kcal",
        "note": None,
        "target": None,
    },
    {
        "title": "Nước (ml)",
        "id": "water",
        "unit": "ml",
        "note": None,
        "target": 2000,
    },
    {
        "title": "Ngủ (giờ)",
        "id": "sleep",
        "unit": "hours",
        "note": None,
        "target": 7,
    },
    {
        "title": "Huyết áp (mmHg/bpm)",
        "id": "bloodpressure",
        "unit": "mmHg/bpm",
        "note": None,
        "target": None,
    }
]

st.set_page_config(
    page_title="Thống kê sức khỏe",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="collapsed"
)



def update(id:str, value, type):
    print("User updated ", type, " key ", id," with value:", value)

root = st.empty()



def detail():
    pass

def dashboard():
    # Initialize day_show in session state if it doesn't exist
    if "day_show" not in st.session_state:
        st.session_state.day_show = {
            "weight": 5,
            "height": 5,
            "kcal": 5,
            "water": 5,
            "sleep": 5,
            "bloodpressure": 5
        }

    # Initialize range_option in session state if it doesn't exist
    if "range_option" not in st.session_state:
        st.session_state.range_option = {
            "weight": "5 ngày",
            "height": "5 ngày",
            "kcal": "5 ngày",
            "water": "5 ngày",
            "sleep": "5 ngày",
            "bloodpressure": "5 ngày"
        }

    st.markdown(
        """
        <h2 style="color: #2e7efb; text-align: center; margin-bottom: 0;">
            📊 Khám phá hành trình sức khỏe của bạn!
        </h2>
        <p style="text-align: center; color: #aaa; font-size: 1.1rem;">
            Theo dõi các chỉ số quan trọng và tiến bộ mỗi ngày để sống khỏe mạnh hơn 💪
        </p>
        """,
        unsafe_allow_html=True
    )


    def _update_range_option(metric_id, new_value):
        st.session_state.range_option[metric_id] = new_value
        # print(f"Updated range option for {metric_id} to {new_value}")

    count = -1
    cols = st.columns([1, 1], gap="medium")

    for idx, metric in enumerate(metrics):
        with cols[idx % 2]:
            count+=1
            with st.container(border=True):
                if st.session_state.range_option[metric["id"]] == "5 ngày":
                    day_show_value = 5
                elif st.session_state.range_option[metric["id"]] == "2 tuần":
                    day_show_value = 14
                elif st.session_state.range_option[metric["id"]] == "1 tháng":
                    day_show_value = 30
                else:
                    day_show_value = 5
                today_str = datetime.date.today().isoformat()
                raw_date = datetime.date.today()
                metric["history"] = builddata.build_range(builddata.calulate_begin_from_end(today_str, day_show_value), today_str , history[metric["id"]], default_none=0)
                metric["value"] = metric["history"][-1] if metric["history"] else 0
                metric["target"] = metric.get("target", 0)
                st.session_state[f"today_user_input_type_{metric['id']}"] = True if history[metric["id"]].get(str(raw_date.year), {}).get(str(raw_date.month), {}).get(str(raw_date.day)) else False


                st.markdown(
                    f"""
                    <div style='
                        border-radius: 18px;
                        background: #262730;
                        padding: 10px 0px 0px 10px;
                        margin-bottom: 18px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        flex-direction: row;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                        width: 100%;
                    '>
                        <h4 style='font-size: xx-large; font-weight: bold'>{metric['title']}</h4>
                        <div style='font-size: 2.5rem; font-weight: bold; color: #2e7efb; margin-bottom: 10px;'>
                            {metric['value']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if all(isinstance(x, (int, float, np.integer, np.floating)) for x in metric["history"]):
                    con_cols = st.columns([2, 3], gap="large")
                    with con_cols[0]:
                        st.write("Chọn mốc thời gian:")
                    with con_cols[1]:
                        range_option = st.segmented_control(
                            "Mốc thời gian",
                            options=["5 ngày", "2 tuần", "1 tháng"],
                            default="5 ngày",
                            label_visibility="collapsed",
                            selection_mode="single",
                            key=f"range_{metric['id']}",
                            on_change=None,
                        )
                        st.session_state.range_option[metric["id"]] = range_option
                        
                        if st.session_state.range_option[metric["id"]] == "5 ngày":
                            day_show_value = 5
                        elif st.session_state.range_option[metric["id"]] == "2 tuần":
                            day_show_value = 14
                        elif st.session_state.range_option[metric["id"]] == "1 tháng":
                            day_show_value = 30
                        else:
                            day_show_value = 5

                    df = pd.DataFrame({
                        "Ngày": [i for i in builddata.build_list_date(builddata.calulate_begin_from_end(today_str, day_show_value), today_str)],
                        "Giá trị": builddata.build_range(builddata.calulate_begin_from_end(today_str, day_show_value), today_str, history[metric["id"]], default_none=0)
                    })
                    fig = px.bar(df, x="Ngày", y="Giá trị", title=metric["title"])

                    data_min = min(metric["history"])
                    data_max = max(metric["history"])
                    buffer = (data_max - data_min) * 0.3
                    y_min = max(0, data_min - buffer)
                    y_max = data_max + buffer

                    if metric.get("target"):
                        fig.add_trace(
                            go.Scatter(
                                x=df["Ngày"],
                                y=[metric["target"]] * len(df),
                                mode="lines",
                                name="Target",
                                line=dict(color="red", width=3, dash="dash")
                            )
                        )

                    fig.update_layout(
                        yaxis_title=metric["title"],
                        showlegend=True,
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
                    )
                    fig.update_yaxes(range=[y_min, y_max])
                    st.plotly_chart(fig, use_container_width=True)

                    if st.button("Xem thêm thông tin >", use_container_width=True, key=f"view_more_detail_type_{metric["id"]}"):
                        pass

                else:
                    st.write("Không thể thể hiện biểu đồ với chỉ số này")

                btn_cols = st.columns([1, 1])

                with btn_cols[0].popover("🎯 Mục tiêu", use_container_width=True):
                    new_target = st.number_input(
                        "Nhập mục tiêu mới:",
                        value=metric.get("target") or 0.0,
                        key=f"input_target_{idx}_0"
                    )
                    if st.button("Lưu", type="secondary", key=f"input_target_type_{metric["id"]}"):
                        update(metric['id'], new_target, "target")

                with btn_cols[1].popover("✏️ Chỉnh sửa" if st.session_state.get(f"today_user_input_type_{metric['id']}", False)  else "➕ Nhập dữ liệu", use_container_width=True):
                    new_target = st.number_input(
                        "Chỉnh sửa" if st.session_state.get(f"today_user_input_type_{metric['id']}", False)  else "Nhập" + " dữ liệu:",
                        key=f"input_target_{idx}_1"
                    )
                    if st.button("Lưu", type="secondary", key=f"input_value_type_{metric['id']}"):
                        update(metric['id'], new_target,"value")

        if idx % 2 == 1 and idx != len(metrics) - 1:
            cols = st.columns([1, 1], gap="medium")

dashboard()

# --- buildata (your buildata code here)
# --- metric (your metric code here)