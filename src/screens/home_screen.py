import streamlit as st
from src.components.footer import footer_home
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_dashboard,style_background_home

def home_screen():
    


    header_home()

    style_background_dashboard()
    style_base_layout()
    style_background_home()

    col1, col2 = st.columns(2,gap="large")

    with col1:
        st.header("I am a Student")
        st.image("https://cdn-icons-png.flaticon.com/512/201/201818.png", width=200)
        if st.button("Student Portal",type="primary",icon=":material/arrow_forward:",icon_position="right"):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        
        st.header("I am a Teacher")
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=200)
        if st.button("Teacher Portal",type="primary",icon=":material/arrow_forward:",icon_position="right"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()