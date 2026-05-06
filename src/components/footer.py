
import streamlit as st

def footer_home():
    st.markdown(
        """
        <div style='display: flex; gap: 1rem; flex-direction: column; align-items: center; justify-content: center; margin-top: 30px;'>
        <p style='font-weight: bold; text-align: center; color:black;'>© Created by ❤️ Saurav Rauthan. All rights reserved.</p>
        </div>  

        """,
        unsafe_allow_html=True
    )

