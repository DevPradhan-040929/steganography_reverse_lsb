import streamlit as st
from PIL import Image
from backend.stego_engine import hide_message, extract_message
from backend.explainability import calculate_capacity, generate_difference_image

st.set_page_config(page_title="Explainable Steganography", layout="wide")

st.title("🔐 Explainable Image Steganography System")

tab1, tab2 = st.tabs(["Hide Message", "Extract Message"])

#  HIDE MESSAGE 
with tab1:
    st.subheader("Hide Secret Message")

    img_file = st.file_uploader("Upload PNG Image", type=["png"])
    secret = st.text_area("Enter Secret Text")

    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Original Image", use_column_width=True)

        capacity = calculate_capacity(image)
        st.info(f"📦 Image Capacity: {capacity} characters")

        if st.button("Hide Message"):

            if len(secret) == 0:
                st.warning("Please enter a secret message.")

            elif len(secret) > capacity:
                st.error("❌ Message too long for this image.")

            else:
                stego = hide_message(image, secret)
                diff = generate_difference_image(image, stego)

                st.image(stego, caption="Stego Image", use_column_width=True)
                st.image(diff, caption="Pixel Difference (Explainability)", use_column_width=True)

                # Save stego image
                stego.save("stego.png")

                # Proper download button
                with open("stego.png", "rb") as file:
                    st.download_button(
                        label="⬇ Download Stego Image",
                        data=file,
                        file_name="stego.png",
                        mime="image/png"
                    )

# EXTRACTION 
with tab2:
    st.subheader("Extract Secret Message")

    stego_file = st.file_uploader("Upload Stego Image", type=["png"], key="extract")

    if stego_file is not None:
        stego_image = Image.open(stego_file)
        st.image(stego_image, caption="Uploaded Stego Image", use_column_width=True)

        if st.button("Extract Message"):
            message = extract_message(stego_image)

            st.success("Hidden Message Extracted:")
            st.code(message)