# modules/notes.py
import streamlit as st
import os
import base64


def show_notes():
    st.header("📚 我的数学笔记")
    st.write("这里是我整理的一些笔记，欢迎交流指正。")

        # 1. 【核心修正】获取当前 notes.py 文件的绝对路径
    # 例如：/mount/src/math_web/web/modules/notes.py
    current_script_path = os.path.abspath(__file__)
    
    # 2. 从这个路径出发，找到它的父目录的父目录，也就是项目的根目录 "web"
    # os.path.dirname() 就像是剥洋葱，剥掉一层
    project_root = os.path.dirname(os.path.dirname(current_script_path))
    
    # 3. 在项目根目录下，拼接出 note_resources 文件夹的绝对路径
    folder_path = os.path.join(project_root, "note_resources")
    if os.path.exists(folder_path):
        all_files = os.listdir(folder_path)
        pdf_files = [f for f in all_files if f.endswith('.pdf')]

        if len(pdf_files) > 0:
            selected_file = st.selectbox("👉 请选择你要查看或下载的笔记：", pdf_files)
            file_path = os.path.join(folder_path, selected_file)

            with open(file_path, "rb") as file:
                file_data = file.read()

            st.download_button(
                label=f"📥 点击下载《{selected_file}》",
                data=file_data,
                file_name=selected_file,
                mime="application/pdf"
            )

            with st.expander("点击展开在线预览"):
                base64_pdf = base64.b64encode(file_data).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.info("文件夹里还没有放入 PDF 笔记哦。")
    else:
        st.error("找不到 resources 文件夹，请检查目录结构！")
