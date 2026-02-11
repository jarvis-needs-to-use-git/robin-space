import streamlit as st
import sys
import os

st.set_page_config(page_title="Robin Space | Debug Mode")

st.title("🔍 Deep Debug Mode")

st.write("Streamlit is running!")
st.write(f"Python Version: {sys.version}")
st.write(f"Executable: {sys.executable}")

def try_import(module_name):
    st.write(f"Attempting to import `{module_name}`...")
    try:
        if module_name == "matplotlib":
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            st.success(f"✅ `{module_name}` imported successfully (Backend: {matplotlib.get_backend()})")
        elif module_name == "meep":
            import meep as mp
            st.success(f"✅ `{module_name}` imported successfully")
        else:
            __import__(module_name)
            st.success(f"✅ `{module_name}` imported successfully")
    except Exception as e:
        st.error(f"❌ Failed to import `{module_name}`")
        st.code(str(e))
    except BaseException as e:
        # Catch system exits, sigterms, etc if possible
        st.error(f"☠️ Critical Failure importing `{module_name}`")
        st.code(str(e))

st.header("Dependency Check")
try_import("numpy")
try_import("matplotlib")
try_import("meep")

st.header("Directory Listing")
st.code(os.listdir("."))
