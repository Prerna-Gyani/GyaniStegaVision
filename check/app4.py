import streamlit as st
from stegano import lsb
from PIL import Image
import tempfile

import google.generativeai as genai

st.set_page_config(page_title="Stegano + Gemini AI", layout="centered")

st.title("🖼️ Steganography + Gemini AI Assistant")

# -------------------------------
# SIDEBAR (API CONFIG)
# -------------------------------
st.sidebar.header("🔑 Gemini API Settings")

api_key = st.sidebar.text_input("Enter Google AI Studio API Key", type="password")
model_name = st.sidebar.text_input("Enter Model Name (e.g. gemini-1.5-flash)")

if api_key:
    genai.configure(api_key=api_key)

# -------------------------------
# ENCODE SECTION
# -------------------------------
st.header("🔐 Encode Text into Image")

uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="encode")
secret_text = st.text_area("Enter text to hide")

if uploaded_image and secret_text:
    image = Image.open(uploaded_image).convert("RGB")

    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(temp_input.name)

    encoded_image = lsb.hide(temp_input.name, secret_text)

    st.image(encoded_image, caption="Encoded Image", use_column_width=True)

    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    encoded_image.save(temp_output.name)

    with open(temp_output.name, "rb") as f:
        st.download_button(
            "📥 Download Encoded Image",
            data=f,
            file_name="encoded.png",
            mime="image/png"
        )

# -------------------------------
# DECODE SECTION
# -------------------------------
st.header("🔍 Decode Hidden Text")

decode_image = st.file_uploader("Upload Encoded Image", type=["png", "jpg", "jpeg"], key="decode")

decoded_text = ""

if decode_image:
    image = Image.open(decode_image).convert("RGB")

    temp_decode = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(temp_decode.name)

    decoded_text = lsb.reveal(temp_decode.name)

    if decoded_text:
        st.success("✅ Hidden Text Found:")
        st.code(decoded_text)
    else:
        st.warning("⚠️ No hidden text detected.")

# -------------------------------
# GEMINI AI SECTION
# -------------------------------
st.header("🤖 Analyze / Ask Questions (Gemini AI)")

user_query = st.text_area("Ask question about decoded text or image")

if st.button("Generate AI Response"):
    if not api_key or not model_name:
        st.error("❌ Please provide API key and model name")
    else:
        try:
            model = genai.GenerativeModel(model_name)

            prompt = f"""
            Hidden Text:
            {decoded_text}

            User Question:
            {user_query}
            """

            response = model.generate_content(prompt)

            st.success("✅ AI Response:")
            st.write(response.text)

        except Exception as e:
            st.error("❌ Error connecting to Gemini API")
