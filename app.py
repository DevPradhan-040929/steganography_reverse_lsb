import streamlit as st
from PIL import Image
from backend.stego_engine import hide_message, extract_message
from backend.explainability import calculate_capacity, generate_difference_image

st.set_page_config(page_title="Explainable Steganography", layout="wide")

st.title("🔐 Explainable Image Steganography System")

tab1, tab2 = st.tabs(["Hide Message", "Extract Message"])

with tab1:
    st.subheader("Hide Secret Message")
    img_file = st.file_uploader("Upload PNG Image", type=["png"])
    secret = st.text_area("Enter Secret Text")

    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Original Image")

        capacity = calculate_capacity(image)
        st.info(f"📦 Image Capacity: {capacity} characters")

        if st.button("Hide Message"):
            stego = hide_message(image, secret)
            diff = generate_difference_image(image, stego)

            st.image(stego, caption="Stego Image")
            st.image(diff, caption="Pixel Difference (Explainability)")

            stego.save("stego.png")
            st.download_button("Download Stego Image", open("stego.png", "rb"))

with tab2:
    st.subheader("Extract Secret Message")
    stego_file = st.file_uploader("Upload Stego Image", type=["png"], key="extract")

    if stego_file and st.button("Extract"):
        stego_image = Image.open(stego_file)
        message = extract_message(stego_image)
        st.success("Hidden Message:")
        st.code(message)
