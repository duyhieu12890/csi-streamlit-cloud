import streamlit as st
import streamlit_app as app
import modules.libbase as libbase
import requests
import pandas as pd
import plotly.express as px
from io import BytesIO
from PIL import Image
app.sidebar_menu()
import time

libbase.load_firebase()


if not st.session_state.get("IS_USER_LOGGED", False):
    st.warning("Bạn cần đăng nhập để sử dụng nhận diện thức ăn.")
    st.stop()

box_note = st.empty()


def get_classify_result(image, api_url="http://127.0.0.1:8000/predict"):
    # Placeholder for actual classification logic
    # This function should return a dictionary with keys: name, id, index, percentage

    file = {"file": image.getvalue()}
    params = {"top_k": 10}

    try:
        response = requests.post(api_url, files=file, params=params)
        print(response.json())
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            st.error("Lỗi khi gọi API phân loại: " + response.text)
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi kết nối đến máy chủ phân loại: {e}")
        return False

db_url = libbase.get_root_db()
list_host = libbase.get_root_db().get()["host"]["model"]
print(list_host)
url = {}
# for host in list_host:
#     print("Getting available model on host", host, "| url:", list_host[host])
#     response = requests.get(list_host[host] + "/available_models")
#     if response.status_code == 200:
#         data_response = response.json()
#         for model in data_response:
#             meta[model] = model + ": " + data_response[model]["description"]

for host in list_host:
    print("Getting available model on host",host,"| url:", list_host[host])
    response = requests.get(list_host[host] + "/available_models")
    if response.status_code == 200:
        data_response = response.json()
        for model in data_response:
            if url.get(model, None) == None: 
                url[model] = {
                    "name": data_response[model]["name"],
                    "description": data_response[model]["description"],
                    "url": list_host[host] + "/" + model
                }
            
# if get_url is None:
#     st.error("Không thể kết nối đến cơ sở dữ liệu Firebase. Vui lòng kiểm tra cấu hình.")
#     print(get_url)

def reverse_dict_multiple_keys(input_dict):
  reversed_dict = {}
  for key, value in input_dict.items():
    if value in reversed_dict:
      reversed_dict[value].append(key)
    else:
      reversed_dict[value] = [key]
  return reversed_dict

def classify():
    # global meta
    st.title("Classify Your Food")
    st.write("Nhận diện thực phẩm của bạn một cách dễ dàng và nhanh chóng.")



    # meta_reverse = reverse_dict_multiple_keys(meta)
    st.set_page_config(layout="wide")
    result = {
        "name": "",
        "id": "",
        "index": "",
        "percentage": 0.0,
    }

    main, stats = st.tabs(["🔎 Dự đoán", "📈 Thống kê"])
    
    wait = False
    with main:
        index = {}
        for i in url:
            index[(url[i]["name"] + ": " + url[i]["description"])] = i
        # meta = {
        #     "UECFOOD256": "UECFOOD256: Model nhận diện thức ăn Nhật Bản và các nước khác (có 1 số món ăn Việt Nam)",
        #     "UECFOOD100": "UECFOOD100: Model nhận diện chủ yếu thức ăn Nhật Bản",
        # }
        select_model = st.selectbox("Lựa chọn model để phân loại thực phẩm của bạn. ⚠️ Lưu ý, chọn sai model có để dẫn tới việc model nhận diện không đúng", 
                     options=[i for i in index], index=0)

        # Placeholder for classification interface
        uploaded_file = st.file_uploader("Tải hình ảnh của bạn lên", type=["jpg", "jpeg", "png"], accept_multiple_files=False, label_visibility="collapsed")
        
        if uploaded_file:
            # # Simulate a classification response (this would be replaced with actual classification logic)
            # st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            # st.write("Classification Result: Example Food Item")
            cols = st.columns([0.4,0.6])
            with cols[0]:
                img_preview = st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

                    

            stats_container = st.container()
            with cols[1]:
                btn_cols = st.columns([0.4, 0.6])
                with btn_cols[0]:
                    button_classify = st.button("Nhận diên thức ăn", key="classify_button", use_container_width=True, icon="🔍")
                with btn_cols[1]:
                    switch_chat_page = st.button("Thêm kết quả vào chatbox",use_container_width=True, icon="🤖", key="add_info_to_chatbox")
                
                if switch_chat_page:    
                    st.session_state['chatbox_switch_from'] = "switch_from_classify"
                    st.session_state['classify_data'] = result
                    st.session_state['trigger_switch_to_chat'] = True
                    print("Switching Chat page...")
                    st.switch_page("pages/chat.py")

                if button_classify:
                    status = st.status("Đang nhận diên ảnh...", expanded=True)
                    with status:
                        with st.spinner("Đang chuẩn bị / xử lý dữ liệu...",show_time=True):
                            file = {"file": uploaded_file.getvalue()}
                            params = {"top_k": 10}
                            # url = "uecfood256" if select_model == meta["UECFOOD256"] else "uecfood100"
                            url_predict = index[select_model]
                            get_url = url[url_predict]["url"]
                            time.sleep(1)
                        st.success("Đã chuẩn bị")

                        with st.spinner("Đang phân loại ảnh, Đợi máy chủ phản hồi...", show_time=True):
                            result = get_classify_result(uploaded_file, api_url=get_url + "/predict")
                            print(result)
                            if not result:
                                st.error("Không thể phân loại ảnh. Vui lòng thử lại sau.")
                                # status.update("Lỗi phân loại ảnh")
                                status.update(label="Lỗi phân loại ảnh", expanded=True, state="error")
                                return
                        st.success("Đẫ phân loại ảnh. Return 200 OK")

                        status.update(label="Đã phân loại ảnh", expanded=False, state="complete")



 
                    st.markdown("### 🎯 Kết quả phân loại")
                    child_cols = st.columns([0.8, 0.2])
                    top_result = result[0]
                    with child_cols[0]:
                        st.write("**Tên thực phẩm dự đoán:**")
                        st.markdown(f"## {top_result['name']}")
                    with child_cols[1]:
                        st.write("**Tỷ lệ chính xác:**")
                        st.markdown(f"## {top_result['percentage']:.2f}%")
            
                    st.markdown(f"""### Mô tả thức ăn:
{top_result['description']}""", unsafe_allow_html=True)
                    st.markdown(f"[🔎 Tìm hiểu thêm trên Google](https://www.google.com/search?q={str(top_result['name']).replace(' ', '+')})")
                    wait = True


    with stats:
        if wait:
            st.header("📊 Top 10 dự đoán của mô hình đưa ra")

            names = [item["name"] for item in result]
            percentages = [item["percentage"] for item in result]\
            
            df = pd.DataFrame({
                "Tên món": names,
                "Xác suất (%)": percentages
            })

            df_sorted = df.sort_values("Xác suất (%)", ascending=True)

            fig = px.bar(
                df_sorted   ,
                x="Xác suất (%)",
                y="Tên món",    
                orientation='h',
                color="Xác suất (%)",
                color_continuous_scale="Blues",
            )

            st.plotly_chart(fig, use_container_width=True)
classify()