import qrcode
import streamlit as st
import io
import PIL

image = PIL.Image.open("app_icon.jpg")

st.set_page_config(page_title="VCARD to QR Code", page_icon=image, layout="centered", initial_sidebar_state="collapsed")

def gen_code(VCARD_str):
    qr_object = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr_object.add_data(VCARD_str)
    qr_object.make(fit=True)

    img = qr_object.make_image(fill_color="black", back_color="white").convert("RGBA")
    return(img)
    # img.save("qrcode.png")

st.title("VCARD Generator")
st.text("Saisir les informations pour générer le QR Code ou coller le code vCard")
VCARD_full = st.text_input("Code vCard")
st.divider()

with st.form("form",enter_to_submit=False):

    lastname = st.text_input("Nom de famille")
    firstname = st.text_input("Prénom")
    
    tel = st.text_input("Téléphone")
    email = st.text_input("Email")

    
    submit = st.form_submit_button("Generer le QR Code")

build = f"""BEGIN:VCARD
VERSION:3.0
N:{lastname};{firstname}
FN:{firstname} {lastname}
TEL;CELL:{tel}
EMAIL:{email}
END:VCARD
"""


if submit and (VCARD_full != "" or build != ""):
    
    if VCARD_full != "":
        VCARD_full = VCARD_full.replace(" ","\n")
        img = gen_code(VCARD_full)
    else:
        img = gen_code(build)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    file_name = ""
    
    if VCARD_full != "":
        file_name = VCARD_full
    else:
        file_name = f"{firstname}_{lastname}"

    
    st.image(img)
    st.download_button(label="Telecharger QR Code", data=img_byte_arr, file_name="qrcode.png", mime="image/png")
