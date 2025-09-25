import streamlit as st
import streamlit.components.v1 as components
from email.message import EmailMessage
from fpdf import FPDF
import tempfile

msg = EmailMessage()
st.write("# Email Generator")

uploaded_files = st.file_uploader(
    "Upload images", accept_multiple_files=True, type=["jpg", "png", "jpeg"]
)

recepient = st.text_input("What is the patient's name?", key="name")

recepient_email = st.text_input("What is the patient's email?", key="email")

template_option = st.radio(
    "What email template would you like to use?",
    ["Permissions", 
    "CER", 
    "Resto"],
    captions=[
        "Permission to send over Treatment Plan",
        "CER template",
        "Resto template",
    ],
    index=None,
)

html_data = ''
path_to_html = False

if template_option == "Permissions":
    path_to_html = "./templates/permissions.html"
    msg['Subject'] = 'Permission to send over Treatment Plan'
elif template_option == "CER":
    path_to_html = "./templates/CER.html"
    msg['Subject'] = 'CER - Comprehensive Exam and Radiographs'
elif template_option == "Resto":
    path_to_html = "./templates/Resto.html"
    msg['Subject'] = 'Restoration'

if path_to_html is not False:
    with open(path_to_html, 'r') as f:
            html_data = f.read()
    components.html(html_data, height=400, scrolling=True)

pdf_bytes = None
if uploaded_files:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    # Add a page with some text at the top
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, f"{recipient} Treatment Plan Images", ln=True, align="C")
    pdf.ln(10)
     
    for uploaded_file in uploaded_files:
        st.image(uploaded_file)

        file_bytes = uploaded_file.read()
        pdf.image(file_bytes.name, x=10, y=30, w=pdf.w - 20)

        # Attach to email
        msg.add_attachment(
            file_bytes,
            maintype="image",
            subtype=uploaded_file.type.split("/")[-1],
            filename=uploaded_file.name,
        )

msg['From'] = 'abhishek21shah@gmail.com'#'drshah.waterfrontdentistry@gmail.com'
msg['To'] = recepient

#msg['text'] = templates['Permissions']
msg.set_content(html_data, subtype='html')
# st.write(msg)
# if st.checkbox("Preview email file"):
#     eml_string = msg.as_string()
#     st.text_area("Email Preview (.eml format)", eml_string, height=300)

msg['X-Unsent'] = '1'

if recepient and recepient_email:
    st.write(f'You are emailing {recepient}. Their email is: {recepient_email}. Is this correct?')
    agree = st.checkbox("Yes")

    if agree:
        st.success("Great! Click the button below to download the email.")
        eml_bytes = msg.as_bytes()
        file_name = f'email_to_{recepient}.eml'
        st.download_button(
                label="Download Email (.eml)",
                data=eml_bytes,
                file_name=file_name,
                mime="message/rfc822"
        )
    