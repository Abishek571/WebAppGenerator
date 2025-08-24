import streamlit as st
import requests

API_URL = "http://localhost:8000"  

st.set_page_config(page_title="Multi-Agent Requirements Analyzer", layout="centered")

st.title("Multi-Agent Requirements Analyzer")
st.write(
    "Upload two requirements documents (PDF, DOCX, MD, or TXT). "
    "The backend will analyze them and generate frontend/backend SRDs (Markdown)."
)

with st.form("upload_form"):
    doc1 = st.file_uploader("Upload first requirements document", type=["pdf", "docx", "md", "txt"], key="doc1")
    doc2 = st.file_uploader("Upload second requirements document", type=["pdf", "docx", "md", "txt"], key="doc2")
    submitted = st.form_submit_button("Analyze Requirements")

if submitted:
    if not doc1 or not doc2:
        st.error("Please upload both documents.")
    else:
        with st.spinner("Analyzing requirements... This may take a few minutes."):
            files = {
                "doc1": (doc1.name, doc1, doc1.type),
                "doc2": (doc2.name, doc2, doc2.type),
            }
            try:
                response = requests.post(f"{API_URL}/analyze-requirements", files=files, timeout=600)
                response.raise_for_status()
                data = response.json()
                st.success("SRDs generated successfully!")
                st.subheader("Frontend SRD (Markdown)")
                st.code(data["frontend_srd_md"], language="markdown")
                st.download_button(
                    label="Download Frontend SRD",
                    data=data["frontend_srd_md"],
                    file_name="srd_frontend.md",
                    mime="text/markdown"
                )
                st.subheader("Backend SRD (Markdown)")
                st.code(data["backend_srd_md"], language="markdown")
                st.download_button(
                    label="Download Backend SRD",
                    data=data["backend_srd_md"],
                    file_name="srd_backend.md",
                    mime="text/markdown"
                )
            except requests.RequestException as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

st.markdown("---")
st.header("Download Previously Generated SRDs")
col1, col2 = st.columns(2)
with col1:
    if st.button("Download Frontend SRD"):
        try:
            resp = requests.get(f"{API_URL}/download-srd/frontend")
            resp.raise_for_status()
            st.download_button(
                label="Download Frontend SRD",
                data=resp.content,
                file_name="srd_frontend.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"Could not download frontend SRD: {e}")

with col2:
    if st.button("Download Backend SRD"):
        try:
            resp = requests.get(f"{API_URL}/download-srd/backend")
            resp.raise_for_status()
            st.download_button(
                label="Download Backend SRD",
                data=resp.content,
                file_name="srd_backend.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"Could not download backend SRD: {e}")

st.markdown("---")
st.info("Ensure the FastAPI backend is running and accessible at the configured URL.")
