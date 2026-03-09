import streamlit as st
from PIL import Image
from backend.stego_engine import hide_message, extract_message
from backend.explainability import calculate_capacity, generate_difference_image
from backend.explainability import calculate_mse
import time
from backend.explainability import show_histogram
from backend.explainability import calculate_psnr
from backend.explainability import calculate_psnr
from backend.explainability import show_lsb_plane
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
                start = time.time()
                stego = hide_message(image, secret)
                end = time.time()

                st.write(f"Embedding Time: {end - start} seconds")
                diff = generate_difference_image(image, stego)

                st.image(stego, caption="Stego Image", use_column_width=True)
                st.image(diff, caption="Pixel Difference (Explainability)", use_column_width=True)
                mse = calculate_mse(image, stego)
                st.markdown(
                   f"<h2 style='color:green;'>MSE between original and stego image: {mse}</h2>",
                    unsafe_allow_html=True
                )
                psnr = calculate_psnr(mse)

                st.markdown(
                   f"<h2 style='color:blue;'>PSNR: {psnr:.2f} dB</h2>",
                   unsafe_allow_html=True
                )
                
                hist_original = show_histogram(image)
                st.pyplot(hist_original)

                hist_stego = show_histogram(stego)
                st.pyplot(hist_stego)
                st.image(show_lsb_plane(stego), caption="LSB Plane Visualization")
                st.write("""
**Difference Map Explanation**

This image represents the amplified pixel difference between the original and stego images. 
Since the algorithm embeds data in the least significant bits of pixels, the actual changes 
are extremely small. 

The visualization scales these differences so that the distribution of modified pixels 
can be observed. The random noise pattern indicates that the embedded data is spread 
across the image without significantly affecting visual quality.
""")
                stego.save("stego.png")

                
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
            start = time.time()
            message = extract_message(stego_image)
            end = time.time()
            st.write(f"Extraction Time: {end - start} seconds")
            st.success("Hidden Message Extracted:")
            st.code(message)


