import streamlit as st
import time
import requests
import json
import uuid
from io import BytesIO

# ==========================================
# 配置区域
# ==========================================
API_BASE_URL = "http://localhost:2983" 

# ==========================================
# CSS 样式 (精简且完整版)
# ==========================================
GHIBLI_STYLES = """
<style>
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stAppViewBlock"] { padding: 0 !important; }
body { background: linear-gradient(135deg, #f5f1e8 0%, #fef8f3 50%, #faf0e6 100%); font-family: 'Georgia', serif; color: #4a6a3a; }
.stApp { background: linear-gradient(135deg, #f5f1e8 0%, #fef8f3 50%, #faf0e6 100%); }
.main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; height: calc(100vh - 2rem); }
div[data-testid="stVerticalBlock"]:has(.card-anchor) { background: rgba(255,255,255,0.95); border: 2px solid #d4a574; border-radius: 15px; padding: 20px; box-shadow: 0 6px 12px rgba(123, 160, 91, 0.1); overflow-y: auto; }
div[data-testid="stVerticalBlock"]:has(.upload-anchor) { border: 2px solid #d4a574; display: flex; flex-direction: column; justify-content: center; align-items: center; }
h1, h2, h3, h4 { color: #6b904b; font-weight: 600; text-shadow: 2px 2px 4px rgba(123, 160, 91, 0.1); }
.stButton > button { background: linear-gradient(135deg, #d4a574 0%, #c19a6b 100%); color: white; border: none; border-radius: 25px; padding: 12px 24px; transition: all 0.3s ease; }

/* 关键词 Tag 样式 */
.keyword-tag {
    display: inline-block;
    background: linear-gradient(135deg, #6b904b 0%, #7ba04b 100%);
    color: white;
    padding: 4px 12px;
    margin: 2px 4px 2px 0;
    border-radius: 15px;
    font-size: 0.85em;
    box-shadow: 0 2px 4px rgba(123, 160, 91, 0.2);
}

.loading-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(255, 253, 245, 0.95); backdrop-filter: blur(8px); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 9999; }
.loading-tomato { font-size: 6rem; animation: rotateBounce 2s infinite ease-in-out; }
@keyframes rotateBounce { 0%, 100% { transform: translateY(0) rotate(0deg); } 25% { transform: translateY(-20px) rotate(5deg); } 50% { transform: translateY(0) rotate(0deg); } 75% { transform: translateY(-10px) rotate(-5deg); } }
.waiting-container { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; color: #7b6345; font-style: italic; }
.pulse-loader { width: 40px; height: 40px; border: 3px solid #d4a574; border-top: 3px solid transparent; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 15px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
"""

# ==========================================
# 核心 API 逻辑
# ==========================================

def upload_paper_api(file_obj):
    try:
        files = {'pdf': (file_obj.name, file_obj, 'application/pdf')}
        response = requests.post(f"{API_BASE_URL}/api/extract", files=files, timeout=120)
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True, 
                'summary': data.get('text', '摘要生成中...'), 
                'prompt': data.get('generatedPrompt', ''),
                'metadata': data.get('metadata', {})
            }
        return {'success': False, 'error': f"HTTP {response.status_code}"}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def generate_stream_api(prompt):
    try:
        payload = {"paperText": prompt}
        response = requests.post(f"{API_BASE_URL}/api/generate/stream", json=payload, stream=True, timeout=180)
        current_event = None
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('event: '):
                    current_event = decoded_line[7:].strip()
                elif decoded_line.startswith('data: '):
                    try:
                        chunk = json.loads(decoded_line[6:])
                        if 'type' not in chunk and current_event:
                            chunk['type'] = current_event
                        yield chunk
                    except:
                        continue
    except Exception as e:
        yield {"type": "error", "error": str(e)}

def render_safe_image(url_path, caption):
    full_url = f"{API_BASE_URL}{url_path}" if not url_path.startswith('http') else url_path
    try:
        r = requests.get(full_url, params={'t': int(time.time())}, timeout=10)
        if r.status_code == 200:
            st.image(r.content, use_container_width=True, caption=caption)
            return r.content 
        return None
    except:
        return None

def reset_app():
    st.session_state.stage = "idle"
    st.session_state.paper_info = {}
    st.session_state.candidates = []
    st.session_state.generated_prompt = ""
    st.session_state.uploader_key = str(uuid.uuid4())

# ==========================================
# 主程序
# ==========================================

def main():
    st.set_page_config(page_title="Micro Tomato", page_icon="🍅", layout="wide")
    st.markdown(GHIBLI_STYLES, unsafe_allow_html=True)
    
    # --- 1. 状态管理 ---
    if 'stage' not in st.session_state: st.session_state.stage = "idle"
    if 'paper_info' not in st.session_state: st.session_state.paper_info = {}
    if 'candidates' not in st.session_state: st.session_state.candidates = []
    if 'generated_prompt' not in st.session_state: st.session_state.generated_prompt = ""
    if 'uploader_key' not in st.session_state: st.session_state.uploader_key = "pdf_upload_init"

    st.markdown('<div style="text-align: center; margin-bottom: 30px; padding: 20px;"><h1 style="font-size: 3em; margin: 0;">Micro Tomato 🍅 学术论文图解助手</h1></div>', unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 1, 1])

    # 1. 左侧：上传
    with col_left:
        with st.container(height=680):
            st.markdown('<div class="upload-anchor"></div><div style="font-size: 3em; margin-bottom: 20px; color: #d4a574; text-align: center;">📁</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("选择PDF文件", type=['pdf'], key=st.session_state.uploader_key)
            
            is_processing = st.session_state.stage in ["parsing", "visualizing"]
            btn_label = "📤 确认上传" if st.session_state.stage != "completed" else "🔄 重新分析"
            
            if st.button(btn_label, key="confirm_upload", use_container_width=True, disabled=(uploaded_file is None or is_processing)):
                if st.session_state.stage == "completed":
                    st.session_state.candidates = []
                st.session_state.stage = "parsing"
                st.rerun()

            if st.session_state.stage == "completed":
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🧹 清空会话", key="clear_all", use_container_width=True):
                    reset_app()
                    st.rerun()

    # 2. 中间：信息 (修复关键词展示)
    with col_center:
        with st.container(height=680):
            st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
            if not st.session_state.paper_info:
                st.markdown('<div class="waiting-container"><div class="waiting-emoji">🍅</div><div>等待您的投喂...</div></div>', unsafe_allow_html=True)
            else:
                info = st.session_state.paper_info
                st.markdown("### 论文解析")
                st.markdown(f"**标题:** {info.get('paper_title')}")
                st.markdown(f"**作者:** {', '.join(info.get('authors', []))}")
                
                # --- 核心修复：补充关键词 Tag 展示 ---
                st.markdown("#### 关键词")
                keywords = info.get('keywords', [])
                if keywords:
                    keywords_html = "".join([f'<span class="keyword-tag">{k}</span>' for k in keywords])
                    st.markdown(f'<div style="line-height: 1.8; margin-bottom: 15px;">{keywords_html}</div>', unsafe_allow_html=True)
                else:
                    st.markdown("*无关键词数据*")
                
                st.markdown("#### AI 摘要")
                st.markdown(f'<div style="background: rgba(255, 255, 255, 0.9); border: 1px solid #e8dcc6; border-radius: 10px; padding: 15px; color: #4a6a3a; line-height: 1.6;">{info.get("summary")}</div>', unsafe_allow_html=True)

    # 3. 右侧：图解区域
    with col_right:
        with st.container(height=680):
            st.markdown('<div class="card-anchor"></div>', unsafe_allow_html=True)
            output_area = st.empty()

            def display_all_candidates(status_msg=None):
                with output_area.container():
                    if status_msg:
                        st.markdown(f'<div class="waiting-container"><div class="pulse-loader"></div><div>{status_msg}</div></div>', unsafe_allow_html=True)
                    
                    if st.session_state.candidates:
                        st.markdown("### 🎨 并列视觉方案")
                        for cand in reversed(st.session_state.candidates):
                            st.markdown(f"**{cand['style_tag']}**")
                            img_data = render_safe_image(cand['image_url'], cand['style_tag'])
                            if st.session_state.stage == "completed" and img_data:
                                st.download_button(
                                    label="Download ⬇️", 
                                    data=img_data, 
                                    file_name=f"plot_{cand['id']}.png", 
                                    key=f"dl_{cand['id']}"
                                )
                            st.markdown("---")
                    elif not status_msg:
                        st.markdown('<div class="waiting-container"><div class="waiting-emoji">🎨</div><div>等待解析完成...</div></div>', unsafe_allow_html=True)

            if st.session_state.stage == "visualizing":
                prompt = st.session_state.generated_prompt
                if prompt:
                    display_all_candidates("AI 画师正在构思...")
                    stream_gen = generate_stream_api(prompt)
                    for chunk in stream_gen:
                        if chunk.get('type') == 'image':
                            img_url = chunk.get('url')
                            if img_url:
                                st.session_state.candidates.append({
                                    'id': str(uuid.uuid4())[:8],
                                    'style_tag': f"方案 {len(st.session_state.candidates) + 1}",
                                    'image_url': img_url
                                })
                                display_all_candidates("正在绘制更多方案...")
                    st.session_state.stage = "completed"
                    st.rerun()
            else:
                if st.session_state.stage == "parsing":
                    output_area.markdown('<div class="waiting-container"><div class="waiting-emoji">📄</div><div>正在阅读论文...</div></div>', unsafe_allow_html=True)
                else:
                    display_all_candidates()

    # --- 后台解析流转 ---
    if st.session_state.stage == "parsing":
        st.markdown(f"""<div class="loading-overlay"><div class="loading-tomato">🍅</div><div class="loading-text">正在深度阅读论文...</div><div class="progress-container"><div class="progress-bar"></div></div></div>""", unsafe_allow_html=True)
        result = upload_paper_api(uploaded_file)
        if result['success']:
            meta = result['metadata']
            st.session_state.paper_info = {
                'paper_title': meta.get('title', uploaded_file.name),
                'authors': meta.get('authors', ['科研团队']),
                'keywords': meta.get('keywords', []),
                'summary': result['summary']
            }
            st.session_state.generated_prompt = result['prompt']
            st.session_state.stage = "visualizing" 
            st.rerun()
        else:
            st.error(f"解析失败: {result.get('error')}")
            st.session_state.stage = "idle"
            st.rerun()

    st.markdown('<div style="text-align: center; padding: 30px 0; margin-top: 40px; color: #7b6345; font-style: italic;">"在数据的森林中，寻找知识的绿洲"</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()