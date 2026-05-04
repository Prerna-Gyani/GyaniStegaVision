import streamlit as st
from stegano import lsb
from PIL import Image
import tempfile

st.set_page_config(page_title="Stegano Image Hiding", layout="centered")

st.title("🖼️ Invisible Image Steganography (LSB - Stegano)")

# -------------------------------
# ENCODE SECTION
# -------------------------------
st.header("🔐 Encode Text into Image")

uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="encode")
secret_text = st.text_area("Enter text to hide")

if uploaded_image and secret_text:
    image = Image.open(uploaded_image).convert("RGB")

    # Save uploaded image temporarily
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(temp_input.name)

    # Encode using Stegano
    encoded_image = lsb.hide(temp_input.name, secret_text)

    st.image(encoded_image, caption="Encoded Image", use_column_width=True)

    # Save encoded image
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    encoded_image.save(temp_output.name)

    with open(temp_output.name, "rb") as f:
        st.download_button(
            "📥 Download Encoded Image",
            data=f,
            file_name="encoded_image.png",
            mime="image/png"
        )

    st.success("✅ Text successfully hidden inside image.")

# -------------------------------
# DECODE SECTION
# -------------------------------
st.header("🔍 Decode Hidden Text")

decode_image = st.file_uploader("Upload Encoded Image", type=["png", "jpg", "jpeg"], key="decode")

if decode_image:
    image = Image.open(decode_image).convert("RGB")

    # Save temp file
    temp_decode = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(temp_decode.name)

    try:
        hidden_text = lsb.reveal(temp_decode.name)

        if hidden_text:
            st.success("✅ Hidden Text Found:")
            st.code(hidden_text)
        else:
            st.warning("⚠️ No hidden text detected.")
    except Exception:
        st.error("❌ Error decoding image.")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("### ⚠️ Notes")
st.markdown("""
- Uses LSB steganography (Stegano)
- Image size and appearance remain unchanged
- Works only for digital images
- ❌ Will NOT work after printing and re-capturing
""")
