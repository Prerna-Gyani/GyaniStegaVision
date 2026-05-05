# GyaniStegaVision

This project is created by Prerna Gyanchandani.

The project consists of two sections:
### 1. The main section - For Print Stegano
### 2. The check section - Stegano, Stegano with Gemini Integration 

===
## Section 1: app.py (DCT)

# 🖼️ Invisible Image Watermarking (DCT-Based)

This project implements frequency-domain watermarking using DCT (Discrete Cosine Transform). It embeds hidden text into an image with minimal visual distortion.

---

## 🚀 Features

- Embed hidden text using DCT  
- No visible perceptual change  
- Same image size maintained  
- Extract hidden data  
- Streamlit-based UI  

---

## 🧠 Concept Used

- Discrete Cosine Transform (DCT)  
- Used in JPEG compression  
- Embeds data in frequency coefficients  

---

## ⚙️ Tech Stack

- Streamlit  
- OpenCV  
- NumPy  
- Pillow  

---

## 📦 Installation

pip install -r requirements.txt

---

## ▶️ Run

streamlit run app.py

---

## ⚠️ Limitations

- Not fully robust to printing and camera capture  
- Sensitive to heavy compression  
- Requires bit-length input  

---

## 📌 Advantages over LSB

- More robust  
- Better for research/demo  
- Less sensitive to minor distortions  

---

---

## Section 2: app3.py (Stegano - LSB)

# 🖼️ Invisible Image Steganography App (Stegano - LSB)

This project demonstrates image steganography using the Stegano library. It allows users to hide and retrieve text inside images without any visible changes.

---

## 🚀 Features

- Hide secret text inside an image  
- No visible change in the image  
- Same image size maintained  
- Extract hidden text from encoded image  
- Simple Streamlit UI  

---

## 🧠 Concept Used

- Least Significant Bit (LSB) Steganography  
- Data is stored in the lowest bits of image pixels  

---

## ⚙️ Tech Stack

- Streamlit  
- Stegano  
- Pillow  

---

## 📦 Installation

pip install -r requirements.txt

---

## ▶️ Run the App

streamlit run app.py

---

## 🌐 Deployment

1. Push code to GitHub  
2. Connect repo to Streamlit Cloud  
3. Click Deploy  

---

## ⚠️ Limitations

- Works only on digital images  
- Does NOT survive printing and camera capture  
- Sensitive to compression and editing  

---

## 📌 Use Cases

- Learning steganography  
- Academic projects  
- Basic secure communication  

---

## 📜 License

Free for educational use
