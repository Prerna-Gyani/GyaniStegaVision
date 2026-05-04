import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile

st.set_page_config(page_title="DCT Image Watermarking", layout="centered")

st.title("🖼️ Invisible Image Watermarking (DCT-Based)")

# -------------------------------
# Helper Functions
# -------------------------------

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ""
    for c in chars:
        try:
            text += chr(int(c, 2))
        except:
            pass
    return text

def embed_dct(image, text):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    img = np.float32(img)

    dct = cv2.dct(img)

    binary = text_to_binary(text)
    length = len(binary)

    h, w = dct.shape
    idx = 0

    for i in range(10, h):
        for j in range(10, w):
            if idx < length:
                if binary[idx] == '1':
                    dct[i][j] += 5
                else:
                    dct[i][j] -= 5
                idx += 1

    idct = cv2.idct(dct)
    idct = np.clip(idct, 0, 255)
    return Image.fromarray(idct.astype(np.uint8)), length


def extract_dct(image, length):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    img = np.float32(img)

    dct = cv2.dct(img)

    bits = ""
    idx = 0

    for i in range(10, dct.shape[0]):
        for j in range(10, dct.shape[1]):
            if idx < length:
                bits += '1' if dct[i][j] > 0 else '0'
                idx += 1

    return binary_to_text(bits)

# -------------------------------
# ENCODE SECTION
# -------------------------------
st.header("🔐 Encode Text into Image")

uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="encode")
text = st.text_area("Enter text to hide")

if uploaded_image and text:
    image = Image.open(uploaded_image).convert("RGB")

    encoded_img, bit_length = embed_dct(image, text)

    st.image(encoded_img, caption="Encoded Image", use_column_width=True)

    # Save temporary file
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    encoded_img.save(temp.name)

    with open(temp.name, "rb") as f:
        st.download_button(
            "📥 Download Encoded Image",
            data=f,
            file_name="encoded.png",
            mime="image/png"
        )

    st.session_state["bit_length"] = bit_length

    st.info("👉 Image looks same, but hidden data is embedded.")

# -------------------------------
# DECODE SECTION
# -------------------------------
st.header("🔍 Decode Hidden Text")

decode_image = st.file_uploader("Upload Encoded / Captured Image", type=["png", "jpg", "jpeg"], key="decode")

length_input = st.number_input("Enter bit length (from encoding step)", min_value=1, step=1)

if decode_image and length_input:
    image = Image.open(decode_image).convert("RGB")

    extracted = extract_dct(image, int(length_input))

    st.success("✅ Extracted Text:")
    st.code(extracted)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("### ⚠️ Notes")
st.markdown("""
- This uses frequency-domain watermarking (DCT)
- Image size and appearance remain nearly identical
- Works best on digital images
- Print → camera recovery may lose some data
""")
