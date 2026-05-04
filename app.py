import streamlit as st
from PIL import Image
import qrcode
import cv2
import numpy as np
import tempfile

st.set_page_config(page_title="Image Steganography (Print-Safe)", layout="centered")

st.title("🖼️ Print-Safe Image Steganography App")

# -------------------------------
# SECTION 1: ENCODE
# -------------------------------
st.header("🔐 Encode Message into Image")

uploaded_image = st.file_uploader("Upload Base Image", type=["png", "jpg", "jpeg"], key="encode")

user_text = st.text_area("Enter text/code to hide")

if uploaded_image and user_text:
    # Load base image
    base_img = Image.open(uploaded_image).convert("RGB")

    # Generate QR
    qr = qrcode.make(user_text)
    qr = qr.convert("RGB")

    # Resize QR
    qr_size = int(min(base_img.size) * 0.25)
    qr = qr.resize((qr_size, qr_size))

    # Optional: reduce visibility (blend)
    qr_np = np.array(qr)
    qr_np = (qr_np * 0.6).astype(np.uint8)  # reduce intensity
    qr = Image.fromarray(qr_np)

    # Paste QR on image
    base_img.paste(qr, (10, 10))

    st.image(base_img, caption="Encoded Image", use_column_width=True)

    # Save temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    base_img.save(temp_file.name)

    with open(temp_file.name, "rb") as file:
        st.download_button(
            label="📥 Download Encoded Image",
            data=file,
            file_name="encoded_image.png",
            mime="image/png"
        )

    st.info("👉 You can now PRINT this image and later capture it using a camera.")

# -------------------------------
# SECTION 2: DECODE
# -------------------------------
st.header("🔍 Decode from Captured Image")

captured_image = st.file_uploader("Upload Captured (Printed) Image", type=["png", "jpg", "jpeg"], key="decode")

if captured_image:
    # Convert to OpenCV format
    file_bytes = np.asarray(bytearray(captured_image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    st.image(img, caption="Uploaded Image", channels="BGR")

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if data:
        st.success("✅ Hidden Data Retrieved:")
        st.code(data)
    else:
        st.error("❌ No hidden data detected. Try clearer image or better lighting.")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("### 💡 Tips for Best Results")
st.markdown("""
- Use high-quality print  
- Avoid glare when capturing image  
- Keep QR area visible (top-left corner)  
- Ensure good lighting  
""")
