
import gradio as gr
import psutil

try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False


def get_system_stats():
    """Fetch CPU and memory stats"""
    memory = psutil.virtual_memory()
    return {
        "CPU Usage (%)": psutil.cpu_percent(interval=1),
        "Memory Used (GB)": round(memory.used / (1024**3), 2),
        "Memory Available (GB)": round(memory.available / (1024**3), 2),
        "Memory Usage (%)": memory.percent
    }


def get_gpu_stats():
    """Fetch GPU stats (if available)"""
    if not GPU_AVAILABLE:
        return {"GPU": "No NVIDIA GPU detected"}

    gpu_data = []
    for i in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        gpu_data.append({
            "Name": pynvml.nvmlDeviceGetName(handle).decode("utf-8"),
            "Memory Total (GB)": round(mem_info.total / (1024**3), 2),
            "Memory Used (GB)": round(mem_info.used / (1024**3), 2),
            "Memory Free (GB)": round(mem_info.free / (1024**3), 2),
            "GPU Utilization (%)": utilization.gpu,
            "Memory Utilization (%)": utilization.memory
        })
    return gpu_data


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🖥️ System Resource Monitor Dashboard")

    with gr.Row():
        sys_btn = gr.Button("Get System Stats")
        gpu_btn = gr.Button("Get GPU Stats")

    sys_output = gr.JSON()
    gpu_output = gr.JSON()

    sys_btn.click(get_system_stats, outputs=sys_output)
    gpu_btn.click(get_gpu_stats, outputs=gpu_output)


if __name__ == "__main__":
    demo.launch()
