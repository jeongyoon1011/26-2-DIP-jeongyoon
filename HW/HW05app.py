
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.ndimage as nd
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="HW05 Object Counting",
    layout="wide"
)

st.title("HW05 - Object Counting")
st.write("Upload an image to count objects using image processing.")

# 사이드바 설정
st.sidebar.header("Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

th_val = st.sidebar.slider(
    "Threshold Value",
    min_value=0,
    max_value=255,
    value=140
)

# 이미지 업로드 후 처리
if uploaded_file is not None:

    # 1. Grayscale
    I = Image.open(uploaded_file).convert("L")
    f = np.array(I)

    # 2. Median Filtering
    f_denoised = signal.medfilt2d(f, 7)

    # 3. Histogram
    st.header("Image Processing Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Original Image")
        st.image(f, clamp=True, use_container_width=True)

    with col2:
        st.subheader("Median Filtering")
        st.image(f_denoised, clamp=True, use_container_width=True)

    with col3:
        st.subheader("Histogram")
        fig, ax = plt.subplots()
        ax.hist(
            f_denoised.ravel(),
            bins=256,
            range=(0, 256),
            color="gray"
        )
        ax.set_xlabel("Pixel Intensity")
        ax.set_ylabel("Frequency")
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)
        plt.close(fig)

    # 4. Thresholding
    f_mask = f_denoised > th_val

    # 5. Connected Component
    labels, nums = nd.label(f_mask)

    st.header("Object Counting Results")

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Binary Mask")
        st.image(
            (f_mask * 255).astype(np.uint8),
            clamp=True,
            use_container_width=True
        )

    with col5:
        st.subheader("Connected Components")
        fig, ax = plt.subplots()
        ax.imshow(labels, cmap="Spectral_r")
        ax.axis("off")
        st.pyplot(fig)
        plt.close(fig)

    # 6. Object Counting
    st.metric("Total Number of Objects", nums)

    cc = np.zeros((nums, 2), dtype=int)

    for i in range(1, nums + 1):
        cc[i-1, 0] = i
        cc[i-1, 1] = np.sum(labels == i)

    if nums > 0:

        st.subheader("Number of Pixels")

        for i in range(nums):
            st.write(
                f"Object {cc[i, 0]}: {cc[i, 1]} pixels"
            )

        # 7. Largest and Smallest Components
        ind_max = np.argmax(cc[:, 1])
        ind_min = np.argmin(cc[:, 1])

        st.header("Largest and Smallest Components")

        col6, col7 = st.columns(2)

        with col6:
            st.subheader("Largest Component")
            largest = (
                labels == cc[ind_max, 0]
            ).astype(np.uint8) * 255

            st.image(
                largest,
                clamp=True,
                use_container_width=True
            )

            st.write(
                f"Object Index: {cc[ind_max, 0]}"
            )
            st.write(
                f"Number of Pixels: {cc[ind_max, 1]}"
            )

        with col7:
            st.subheader("Smallest Component")
            smallest = (
                labels == cc[ind_min, 0]
            ).astype(np.uint8) * 255

            st.image(
                smallest,
                clamp=True,
                use_container_width=True
            )

            st.write(
                f"Object Index: {cc[ind_min, 0]}"
            )
            st.write(
                f"Number of Pixels: {cc[ind_min, 1]}"
            )

    else:
        st.warning("No objects detected.")

else:
    st.info("Please upload an image from the sidebar.")
