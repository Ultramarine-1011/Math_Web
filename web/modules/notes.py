# modules/notes.py
import streamlit as st
import os
import base64


def show_notes(project_root):
    """
    显示笔记资源模块。
    :param project_root: 从 app.py 传入的项目根目录绝对路径
    """
    st.header("📚 我的数学笔记")
    st.write("这里是我整理的一些笔记，欢迎交流指正。")

    # 【核心修正】拼接绝对路径：项目根目录 + note_resources 文件夹
    folder_path = os.path.join(project_root, "note_resources")

    # 1. 检查 note_resources 文件夹是否存在
    if os.path.exists(folder_path):
        # 2. 获取所有 PDF 文件
        all_files = os.listdir(folder_path)
        pdf_files = [f for f in all_files if f.endswith('.pdf')]

        if len(pdf_files) > 0:
            # 3. 下拉菜单选择
            selected_file = st.selectbox("👉 请选择你要查看或下载的笔记：", pdf_files)

            # 4. 拼接被选中文件的绝对路径
            file_path = os.path.join(folder_path, selected_file)

            # 5. 读取文件
            with open(file_path, "rb") as file:
                file_data = file.read()

            # 6. 下载按钮
            st.download_button(
                label=f"📥 点击下载《{selected_file}》",
                data=file_data,
                file_name=selected_file,
                mime="application/pdf"
            )

            # 7. 在线预览功能 (通过 iframe 渲染)
            with st.expander("点击展开在线预览"):
                base64_pdf = base64.b64encode(file_data).decode('utf-8')
                # 这是一个嵌入 PDF 的 HTML 标签
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.info("文件夹里还没有放入 PDF 笔记哦。")
    else:
        st.error(f"找不到文件夹: {folder_path}，请检查 GitHub 仓库中是否有名为 note_resources 的文件夹！")