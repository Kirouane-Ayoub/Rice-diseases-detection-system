import streamlit as st 
import os 
from PIL import Image
from streamlit_objectDetect import detect
from ob_detect import run
import time 
model_path = "RICE_DECE.pt"
select_type_detect = st.sidebar.selectbox("Detection from :  ",("File", "Live"))

select_device = st.sidebar.selectbox("Select compute Device :  ",("CPU", "GPU"))
crops = st.sidebar.selectbox("Do you want to Save crops ?   :",(False, True))
if select_device == "GPU" : 
    DEVICE_NAME = 0 
elif select_device =="CPU" : 
    DEVICE_NAME = "cpu"

save_output_video = st.sidebar.radio("Save output video?",('Yes', 'No'))
if save_output_video == 'Yes':
    nosave = False
    display_labels=True
else:
    nosave = True
    display_labels = True
conf_thres = st.sidebar.slider("Class confidence threshold" , max_value=1.0 , min_value=0.1)
def fromvid(source, conf_thres , device , vid_id , nosave  , display_labels) :
    kpi5, kpi6 = st.columns(2)
    with kpi5:
        st.markdown("""<h5 style="color:white;">
                                  CPU Utilization</h5>""", 
                                  unsafe_allow_html=True)
        kpi5_text = st.markdown("0")
    with kpi6:
        st.markdown("""<h5 style="color:white;">
                                Memory Usage</h5>""", 
                                unsafe_allow_html=True)
        kpi6_text = st.markdown("0")
    stframe = st.empty()
    detect(weights=model_path,
                   source=source,
                   stframe=stframe, 
                   kpi5_text=kpi5_text , 
                   kpi6_text=kpi6_text, 
                   conf_thres=float(conf_thres),
                   device=device,
                   hide_labels=False,  
                   hide_conf=False,
                   project=vid_id, 
                   nosave=nosave, 
                   display_labels=display_labels)

if select_type_detect == "File" :
    tab0 , tab1, tab2 = st.tabs(["HOME" , "Image", "Video"])
    with tab0 : 
        st.image("icon2.png" , width=500)
        st.info("This APP can detect some rice-diseases using YOLO algorithm ")
        st.header("About Dataset : ")
        st.write("""This is the dataset used by me and my thesis mates when we created a Image Recognition application. 
        they are sorted by diseases and labeled using Labelimg""")
        st.text("""We covered the following diseases for rice plants:
1/ Bacterial Leaf Blight ( BLB )
2/ Blast
3/ Brown spot""")
        st.write("""The datasets provided here are of optimium age (3 to 4 weeks). 
        this is because a disease that is too old or too young cannot be accurately detected. 
        it would need additional data to do so (weather,water sample,leaf sample tests,etc)""")
        st.write("https://github.com/Kirouane-Ayoub/RiceDiseases-DataSet")
    with tab1:
        st.image("icon2.png" , width=200)
        image_id = str(time.asctime())
        st.header("Image")
        image_upload = st.file_uploader("upload your image" , type=["png" , "jpg" , "jpeg"])
        try : 
            run(weights=model_path, source=image_upload.name, 
            device=DEVICE_NAME ,name=image_id , save_crop=crops)
            image = Image.open(f"{image_id}/{image_upload.name}")
            st.image(image)
        except : 
            pass
    
    with tab2 :
        st.image("icon2.png" , width=300)
        vid_id = str(time.asctime())
        st.header("Video")
        video_upload = st.file_uploader("upload your Video" , type=['mp4', 'mov'])
        if video_upload : 
            if st.button('Click to Start'):
                #n_class = tuple(map(int, classes.split(', ')))
                fromvid(source=video_upload.name ,  vid_id=vid_id , device=DEVICE_NAME , conf_thres=conf_thres ,
                 nosave=nosave , display_labels=display_labels)
                
                

elif select_type_detect == "Live" : 
    tab1, tab2 = st.tabs(["URL", "LOCAL-CAM"])
    with tab1 : 
        st.image("icon2.png" , width=200)
        live_id = str(time.asctime())
        url = st.text_input('Entre your URL stream and click enter : ')
        if url : 
            if st.button('Run Detection' , key="uu"): 
                fromvid(source=url , vid_id=live_id , device=DEVICE_NAME , conf_thres=conf_thres ,
                        nosave=nosave , display_labels=display_labels )
    with tab2 : 
        st.image("icon2.png" , width=200)
        cam_id = str(time.asctime())
        index = st.selectbox("Select Device index : " , (0, 1 , 2))
        if st.button('Run Detection'):           
            os.system(f"python objd_tracking.py --source {index} --view-img --conf-thres {conf_thres} --device {DEVICE_NAME} --project '{cam_id}' --color-box")
