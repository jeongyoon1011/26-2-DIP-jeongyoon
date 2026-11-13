import streamlit as st
from PIL import Image
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="My Profile",
    page_icon="👩‍💻",
    layout="wide"
)

# 화면 여백 및 디자인 설정
st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        max-width: 1000px;
    }
</style>
""", unsafe_allow_html=True)

# 사진과 프로필 정보를 나란히 배치
col1, col2 = st.columns([1, 2.5], gap="large")

with col1:
    image = Image.open(Path(__file__).parent / "profile.jpg")
    st.image(image, use_container_width=True)

with col2:

    st.header("JeongYoon Kim")

    st.markdown(
        "<p style='color:gray; font-size:15px;'>"
        "Department of Biomedical Engineering, "
        "Hankuk University of Foreign Studies (HUFS)"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("**Major**")
    st.write("Biomedical Engineering")
