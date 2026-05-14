# import streamlit as st
# from src.database.db import check_teacher_exists,teacher_login,create_teacher,hash_pass,get_teacher_subjects,get_attendance_for_teacher
# from src.components.dialog_create_subject import create_subject_dialog
# from src.components.dialog_share_subject import share_subject_dialog

# from src.ui.base_layout import style_background_dashboard,style_base_layout
# from src.components.header import header_dashboard
# from src.components.footer import footer_dashboard
# from src.components.subject_card import subject_card

# from src.components.dialog_add_photo import add_photos_dialog
# import numpy as np
# from src.pipelines.face_pipeline import predict_attendance
# from src.components.dialog_attendance_results import attendance_result_dialog

# from datetime import datetime
# from src.database.config import supabase
# import pandas as pd
# from src.components.dialog_voice_attendance import voice_attendance_dialog


# def teacher_screen():
#     style_base_layout()
#     style_background_dashboard()
#     if 'teacher_data' in st.session_state:
#         teacher_dashboard()
    
#     elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
#          teacher_screen_login()
#     elif st.session_state.teacher_login_type=='register':
#         teacher_screen_register()          
        
# def teacher_dashboard():
#     teacher_data=st.session_state.teacher_data
#     c1,c2=st.columns(2,vertical_alignment="center",gap="xxlarge")

#     with c1:
#         header_dashboard()

#     with c2:
#         st.subheader(f"""Welcome back, {teacher_data['name']}""")
#         if st.button("Logout",type="secondary",key='loginbackbtn',shortcut="control + backspace"):
#             st.session_state['is_logged_in'] = False
#             del st.session_state.teacher_data
#             st.rerun()

#     st.space()
#     if "current_teacher_tab" not in st.session_state:
#         st.session_state.current_teacher_tab='take_attendance'

#     tab1,tab2,tab3=st.columns(3)

#     with tab1:
#         type1='primary' if st.session_state.current_teacher_tab =='take_attendance' else 'tertiary'
#         if st.button('Take Attendance',type=type1,width='stretch',icon=':material/ar_on_you:'):
#             st.session_state.current_teacher_tab='take_attendance'
#             st.rerun()

#     with tab2:
#         type2='primary' if st.session_state.current_teacher_tab =='manage_subjects' else 'tertiary'
#         if st.button('Manage_Subjects',type=type2,width='stretch',icon=':material/book_ribbon:'):
#             st.session_state.current_teacher_tab='manage_subjects'
#             st.rerun()
            

    
#     with tab3:
#         type3='primary' if st.session_state.current_teacher_tab =='attendance_records' else 'tertiary'
#         if st.button('Attendance Records',type=type3,width='stretch',icon=':material/cards_stack:'):
#             st.session_state.current_teacher_tab='attendance_records'
#             st.rerun()
            

#     st.divider()


#     if st.session_state.current_teacher_tab=='take_attendance':
#         teacher_tab_take_attendance()

#     if st.session_state.current_teacher_tab=='manage_subjects':
#         teacher_tab_manage_subjects()

#     if st.session_state.current_teacher_tab=='attendance_records':
#         teacher_tab_attendance_records()




#     footer_dashboard()

# def teacher_tab_take_attendance():
#     teacher_id=st.session_state.teacher_data['teacher_id']
#     st.header('Take AI Attendance')

#     if 'attendance_images' not in st.session_state:
#         st.session_state.attendance_images=[]

#     subjects=get_teacher_subjects(teacher_id)


#     if not subjects:
#         st.warning('You havent created any subejcts yet! Please create one to begin!')
#         return 
#     subject_options={f"{s['name']} - {s['subject_code']}":s['subject_id'] for s in subjects}

#     col1,col2=st.columns([3,1],vertical_alignment='bottom')

#     with col1:
#         selected_subject_label=st.selectbox('Select Subject',options=list(subject_options.keys()))

#     with col2:
#         if st.button('Add Photos',type='primary',icon=":material/add_a_photo:",width='stretch'):
#             add_photos_dialog()
        
#     selected_subject_id=subject_options[selected_subject_label]





#     st.divider()

#     if st.session_state.attendance_images:
#         st.header('Added Photos')
#         gallery_cols=st.columns(4)

#         for idx,img in enumerate(st.session_state.attendance_images):
#             with gallery_cols[idx % 4]:
#                 st.image(img,width='stretch',caption=f'Photo {idx+1}')

#     has_photos=bool(st.session_state.attendance_images)  
#     c1,c2,c3=st.columns(3)

#     with c1:
#         if st.button('Clear all Photos',width='stretch',type='tertiary',icon=':material/delete:',disabled=not has_photos):
#             st.session_state.attendance_images=[]
#             st.rerun()
        
#     with c2:
        
#         if st.button('Run Face Analysis',width='stretch',type='secondary',icon=':material/analytics:',disabled=not has_photos): 
#             with st.spinner('Deep scanning classroom photos....'):
#                 all_detected_id={}

#                 for idx,img in enumerate(st.session_state.attendance_images):
#                     img_np=np.array(img.convert('RGB'))

#                     detected,_,_=predict_attendance(img_np)

#                     if detected:
#                         for sid in detected.keys():
#                             student_id=int(sid)
#                             all_detected_id.setdefault(student_id,[]).append(f'Photo {idx+1}')
                
#                 enrolled_res=supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_subject_id).execute()


#                 enrolled_students=enrolled_res.data
#                 if not enrolled_students:
#                     st.warning('No Students enrolled in this course')
#                 else:

#                     results,attendance_to_log=[],[]

#                     current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

#                     for node in enrolled_students:
#                         student=node['students']
#                         sources=all_detected_id.get(int(student['student_id']))
#                         is_present=len(sources) > 0

#                         results.append({
#                             "Name":student['name'],
#                             "ID":student['student_id'],
#                             "Source": ", ".join(sources) if is_present else "-",
#                             "Status":"✅ Present" if is_present else " ❌ Absent"
#                         })


#                         attendance_to_log.append({
#                             'student_id':student['student_id'],
#                             'subject_id':selected_subject_id,
#                             'timestamp':current_timestamp,
#                             'is_present':bool(is_present)
#                         })

                

#                 attendance_result_dialog(pd.DataFrame(results),attendance_to_log)

#     with c3:
#         if st.button('Use Voice Attendance',type='primary',width='stretch',icon=':material/mic:'):
#             voice_attendance_dialog(selected_subject_id)







     


# # def teacher_tab_take_attendance():
# #     st.header('Take AI Attendance')

# def teacher_tab_manage_subjects():
#     teacher_id=st.session_state.teacher_data['teacher_id']
#     col1,col2=st.columns(2)

#     with col1:
#         st.header('Manage Subjects',width="stretch")

#     with col2:
#         if st.button('Create New Subjects',width ="content"):
#             create_subject_dialog(teacher_id)
  


#     subjects=get_teacher_subjects(teacher_id)
#     if subjects:
#         for sub in subjects:
#             stats=[
#                 ("👩‍🎓",'Students',sub['total_students']),
#                 ("👨‍💻",'Classes',sub['total_classes']),
#             ]
#         def share_btn():
#             if st.button(f"Share Code:{sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
#                 share_subject_dialog(sub['name'],sub['subject_code'])

#             st.space()
#         subject_card(
#             name=sub['name'],
#             code=sub['subject_code'],
#             section=sub['section'],
#             stats=stats,
#             footer_callback=share_btn


#         )
#     else:
#         st.info("NO SUBJECTS FOUND.CREATE ONE ABOVE")


# def teacher_tab_attendance_records():
#     st.header('Attendance_Records')
#     teacher_id=st.session_state.teacher_data['teacher_id']
#     records=get_attendance_for_teacher(teacher_id)

#     if not records:
#         st.info("No attendance records found.")

#     data=[]

#     for r in records:
#         ts=r.get('timestamp')
#         data.append({
#             "ts_group": ts.split(".")[0] if ts else "N/A",
#             "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
#             "Subject":r['subjects']['name'],
#             "Subject Code": r['subjects']['subject_code'],
#             "is_present": bool(r.get('is_present', False))
#         })

#     df=pd.DataFrame(data)

#     summary=(
#         df.groupby(['ts_group','Time','Subject','Subject Code'])
#         .agg(
#             Present_Count=('is_present','sum'),
#             Total_Count=('is_present','count')
#         ).reset_index()
#     )

#     summary["Attendance Stats"]=(
#         "✅ " + summary['Present_Count'].astype(str) + " / " + "🗓️ " + summary['Total_Count'].astype(str) + 'Students'
#     )

#     display_df=(summary.sort_values(by='ts_group',ascending=False)
#                 [['Time','Subject','Subject Code','Attendance Stats']]
                
#                 )
#     st.dataframe(display_df,hide_index=True,width='stretch')




# def login_teacher(teacher_username, teacher_password):
#     if not teacher_username or not teacher_password:
#         st.error("Please enter both username and password.")
#         return False
    
#     teacher=teacher_login(teacher_username, teacher_password)
#     if teacher:
#         st.session_state.user_role = 'teacher'

#         st.session_state.teacher_data = teacher
#         st.session_state.logged_in = True
#         return True
#     return False

        
    
# def teacher_screen_login():
#     c1,c2=st.columns(2,vertical_alignment="center",gap="xxlarge")

#     with c1:
#         header_dashboard()

#     with c2:
#         if st.button("Go back to home",type="secondary",key='loginbackbtn',shortcut="control + backspace"):
#             st.session_state['login_type'] = None
#             st.rerun()

#     st.header("Login to your teacher profile here",text_alignment="center")
#     st.space()
#     st.space()


#     teacher_username=st.text_input("Username",placeholder="Enter your username here")
#     teacher_password=st.text_input("Password",placeholder="Enter your password here",type="password")

#     st.divider()

#     btnc1,btnc2=st.columns(2)
#     with btnc1:
#         if st.button("Login",icon=":material/passkey:",shortcut="control + enter",width="stretch"):
#             if login_teacher(teacher_username, teacher_password):
#                 st.toast("Login successful!",icon="👍")
#                 import time
#                 time.sleep(1)
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password. Please try again.")

#     with btnc2:
#         if st.button("Register",icon=":material/person_add:",type="primary",width="stretch"):
#             st.session_state['teacher_login_type'] = 'register'
#             st.rerun()



#     footer_dashboard()



# def register_teacher(teacher_username, teacher_password,teacher_name,teacher_password_confirm):
#     if not teacher_username or not teacher_password or not teacher_name or not teacher_password_confirm:
#         return False,"Please fill in all the fields."
#     if check_teacher_exists(teacher_username):
#         return False,"Username already exists. Please choose a different username."
#     if teacher_password != teacher_password_confirm:
#         return False,"Passwords do not match. Please re-enter your password."
#     try:
#         create_teacher(teacher_username, teacher_password,teacher_name)
#         return True,"Teacher account created successfully! Please proceed to login."
#     except Exception as e:
#         return False,f"An error occurred while creating your account: {str(e)}"
   

# def teacher_screen_register():
#     c1,c2=st.columns(2,vertical_alignment="center",gap="xxlarge")

#     with c1:
#         header_dashboard()

#     with c2:
#         if st.button("Go back to home",type="secondary",key='loginbackbtn',shortcut="control + backspace"):
#             st.session_state['login_type'] = None
#             st.rerun()

#     st.header("Register your teacher profile here")
#     st.space()
#     st.space()
    

#     teacher_username=st.text_input("Username",placeholder="Enter your username here")
#     teacher_name=st.text_input("Full Name",placeholder="Enter your full name here")
#     teacher_password=st.text_input("Password",placeholder="Enter your password here",type="password")

#     teacher_password_confirm=st.text_input("Confirm Password",placeholder="Re-enter your password here",type="password")    


#     st.divider()

#     btnc1,btnc2=st.columns(2)
#     with btnc1:
#         if st.button("Register",icon=":material/passkey:",shortcut="control + enter",width="stretch"):
#             success,message=register_teacher(teacher_username, teacher_password,teacher_name,teacher_password_confirm)
#             if success:
#                 st.success(message)
#                 import time
#                 time.sleep(2)
#                 st.session_state['teacher_login_type'] = 'login'
#                 st.rerun()
#             else:
#                 st.error(message)
#     with btnc2:
#         if st.button("Login",icon=":material/person_add:",type="primary",width="stretch"):
#             st.session_state['teacher_login_type'] = 'login'
#             st.rerun()



#     footer_dashboard()





import streamlit as st
from src.database.db import check_teacher_exists, teacher_login, create_teacher, hash_pass, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.components.dialog_add_photo import add_photos_dialog
import numpy as np
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog

from datetime import datetime
from src.database.config import supabase
import pandas as pd
from src.components.dialog_voice_attendance import voice_attendance_dialog


def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome back, {teacher_data['name']}")
        if st.button("Logout", type="secondary", key='loginbackbtn', shortcut="control + backspace"):
            st.session_state['is_logged_in'] = False
            if 'teacher_data' in st.session_state:
                del st.session_state.teacher_data
            st.rerun()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == 'attendance_records':
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You haven\'t created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}
    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=":material/add_a_photo:", width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Photo {idx+1}')

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all Photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos....'):
                all_detected_id = {}
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_id.setdefault(student_id, []).append(f'Photo {idx+1}')

                enrolled_res = supabase.table('subject_students').select("*,students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No Students enrolled in this course')
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().isoformat()

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_id.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else " ❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)

    with col1:
        st.header('Manage Subjects')

    with col2:
        if st.button('Create New Subject', width="content"):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👩‍🎓", 'Students', sub.get('total_students', 0)),
                ("👨‍💻", 'Classes', sub.get('total_classes', 0)),
            ]

            def share_btn(s_name=sub['name'], s_code=sub['subject_code']):
                if st.button(f"Share Code: {s_code}", key=f"share_{s_code}", icon=":material/share:"):
                    share_subject_dialog(s_name, s_code)

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Attendance Records')
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found.")
        return

    data = []
    for r in records:
        ts = r.get('timestamp')
        try:
            # Corrected method name: fromisoformat
            dt_obj = datetime.fromisoformat(ts)
            formatted_time = dt_obj.strftime("%Y-%m-%d %I:%M %p")
            ts_group = ts.split(".")[0] # Grouping key
        except:
            formatted_time = "N/A"
            ts_group = "N/A"

        data.append({
            "ts_group": ts_group,
            "Time": formatted_time,
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)
    
    if df.empty:
        st.warning("No data to display.")
        return

    # Aggregating records by the timestamp group
    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ " + summary['Present_Count'].astype(str) + " / " + summary['Total_Count'].astype(str) + " Students"
    )

    # Corrected 'by' argument and column selection
    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']])
    
    st.dataframe(display_df, hide_index=True, use_container_width=True)


def login_teacher(teacher_username, teacher_password):
    if not teacher_username or not teacher_password:
        st.error("Please enter both username and password.")
        return False
    
    teacher = teacher_login(teacher_username, teacher_password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.logged_in = True
        return True
    return False


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type="secondary", key='loginbackbtn', shortcut="control + backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login to your teacher profile here")
    teacher_username = st.text_input("Username", placeholder="Enter your username here")
    teacher_password = st.text_input("Password", placeholder="Enter your password here", type="password")

    st.divider()
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Login", icon=":material/passkey:", shortcut="control + enter", width="stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login successful!", icon="👍")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")
    with btnc2:
        if st.button("Register", icon=":material/person_add:", type="primary", width="stretch"):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun()


def register_teacher(teacher_username, teacher_password, teacher_name, teacher_password_confirm):
    if not teacher_username or not teacher_password or not teacher_name or not teacher_password_confirm:
        return False, "Please fill in all the fields."
    if check_teacher_exists(teacher_username):
        return False, "Username already exists."
    if teacher_password != teacher_password_confirm:
        return False, "Passwords do not match."
    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Account created successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type="secondary", key='regbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your teacher profile here")
    teacher_username = st.text_input("Username")
    teacher_name = st.text_input("Full Name")
    teacher_password = st.text_input("Password", type="password")
    teacher_password_confirm = st.text_input("Confirm Password", type="password")

    st.divider()
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Register", type="primary", width="stretch"):
            success, message = register_teacher(teacher_username, teacher_password, teacher_name, teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state['teacher_login_type'] = 'login'
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button("Back to Login", width="stretch"):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()


