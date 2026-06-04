import warnings
import os
import logging
import html

# 1. CHẶN LOG NGAY LẬP TỨC TRƯỚC KHI IMPORT BẤT CỨ THỨ GÌ KHÁC
warnings.filterwarnings("ignore")
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTHONWARNINGS"] = "ignore"

# Chặn log từ module logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("langchain").setLevel(logging.ERROR)

import streamlit as st
import pandas as pd
import psycopg2.errors
from database import (
    authenticate_parent,
    get_student_info,
    get_grades,
    get_attendance,
    get_tuition,
    get_teacher_comments,
    get_recent_ai_audit_logs,
)
from agent_langchain import call_langchain_agent
from llm_provider import get_llm_api_key, get_llm_display_name
import time

st.set_page_config(page_title="Hỗ trợ Phụ huynh - VinSchool/VinUni", page_icon="🏫", layout="centered")

st.markdown("""
<style>
.chat-container { border-radius: 10px; padding: 10px; }
.agent-trace-shell {
    margin-top: 0.55rem;
    max-width: 92%;
}
.agent-trace-disclosure {
    border: 1px solid rgba(148, 163, 184, 0.26);
    border-radius: 18px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 252, 0.96));
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
    overflow: hidden;
}
.agent-trace-disclosure[open] {
    border-color: rgba(59, 130, 246, 0.24);
    box-shadow: 0 14px 34px rgba(37, 99, 235, 0.08);
}
.agent-trace-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.9rem;
    padding: 0.78rem 0.95rem;
    cursor: pointer;
    list-style: none;
    background:
        radial-gradient(circle at top left, rgba(219, 234, 254, 0.6), transparent 42%),
        linear-gradient(180deg, rgba(248, 250, 252, 0.98), rgba(255, 255, 255, 0.98));
}
.agent-trace-summary::-webkit-details-marker {
    display: none;
}
.agent-trace-summary-main {
    min-width: 0;
}
.agent-trace-kicker {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.18rem 0.5rem;
    border-radius: 999px;
    background: rgba(219, 234, 254, 0.9);
    color: #1d4ed8;
    font-size: 0.72rem;
    font-weight: 700;
}
.agent-trace-summary-text {
    margin-top: 0.38rem;
    font-size: 0.84rem;
    line-height: 1.45;
    color: #334155;
}
.agent-trace-summary-meta {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    flex-wrap: wrap;
    justify-content: flex-end;
}
.agent-trace-chip {
    padding: 0.22rem 0.58rem;
    border-radius: 999px;
    background: rgba(241, 245, 249, 0.95);
    color: #475569;
    font-size: 0.72rem;
    font-weight: 700;
}
.agent-trace-header {
    display: none;
}
.agent-trace-live {
    padding: 0.22rem 0.58rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #9a3412;
    background: rgba(255, 237, 213, 0.95);
}
.agent-trace-panel {
    padding: 0 0.95rem 0.92rem;
}
.agent-trace-steps-inline {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.2rem;
}
.agent-trace-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.42rem;
    padding: 0.38rem 0.66rem;
    border-radius: 999px;
    background: rgba(248, 250, 252, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.2);
    color: #334155;
    font-size: 0.76rem;
    line-height: 1;
}
.agent-trace-pill-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
}
.agent-trace-details {
    margin-top: 0.75rem;
    display: grid;
    gap: 0.55rem;
}
.agent-trace-step {
    display: flex;
    gap: 0.72rem;
    align-items: flex-start;
    padding: 0.78rem 0.85rem;
    border-radius: 14px;
    background: rgba(248, 250, 252, 0.92);
    border: 1px solid rgba(226, 232, 240, 0.9);
}
.agent-trace-dot {
    width: 10px;
    height: 10px;
    margin-top: 0.42rem;
    border-radius: 999px;
    flex: 0 0 auto;
}
.agent-trace-dot-thinking { background: #2563eb; }
.agent-trace-dot-decision { background: #7c3aed; }
.agent-trace-dot-tool { background: #ea580c; }
.agent-trace-dot-observation { background: #0891b2; }
.agent-trace-dot-answer { background: #16a34a; }
.agent-trace-step-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #0f172a;
}
.agent-trace-step-detail {
    margin-top: 0.16rem;
    font-size: 0.78rem;
    line-height: 1.5;
    color: #334155;
}
.agent-trace-tools-label {
    margin-top: 0.85rem;
    font-size: 0.78rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.agent-tool-card {
    margin-top: 0.55rem;
    border: 1px solid rgba(226, 232, 240, 0.95);
    border-radius: 14px;
    background: rgba(248, 250, 252, 0.92);
    overflow: hidden;
}
.agent-tool-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.7rem;
    padding: 0.72rem 0.88rem;
    cursor: pointer;
    list-style: none;
}
.agent-tool-summary::-webkit-details-marker {
    display: none;
}
.agent-tool-name {
    font-size: 0.8rem;
    font-weight: 700;
    color: #0f172a;
}
.agent-tool-status {
    padding: 0.2rem 0.56rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
}
.agent-tool-status-running {
    color: #b45309;
    background: rgba(254, 243, 199, 0.95);
}
.agent-tool-status-completed {
    color: #166534;
    background: rgba(220, 252, 231, 0.95);
}
.agent-tool-body {
    padding: 0 0.88rem 0.88rem;
}
.agent-tool-caption {
    margin: 0.3rem 0 0.2rem;
    font-size: 0.72rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.agent-tool-pre {
    margin: 0;
    padding: 0.72rem 0.8rem;
    border-radius: 12px;
    background: #0f172a;
    color: #e2e8f0;
    font-size: 0.74rem;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-word;
    overflow-x: auto;
    max-height: 220px;
}
.stMetric {
    border: 1px solid rgba(226, 232, 240, 0.95);
    border-radius: 10px;
    padding: 0.85rem 0.95rem;
    background: rgba(248, 250, 252, 0.72);
}
div[role="radiogroup"] {
    gap: 0.35rem;
}
div[role="radiogroup"] label {
    border: 1px solid rgba(226, 232, 240, 0.95);
    border-radius: 999px;
    padding: 0.28rem 0.72rem;
    background: rgba(255, 255, 255, 0.9);
}
@media (max-width: 640px) {
    .agent-trace-shell {
        max-width: 100%;
    }
    .agent-trace-summary {
        align-items: flex-start;
        flex-direction: column;
    }
    .agent-trace-summary-meta {
        justify-content: flex-start;
    }
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["parent_info"] = None
    st.session_state["student_data"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []


TRACE_KIND_LABELS = {
    "thinking": "Phân tích",
    "decision": "Quyết định",
    "tool": "Thực thi",
    "observation": "Dữ liệu",
    "answer": "Phản hồi",
}


def build_agent_trace_html(trace_steps, tool_calls, live=False):
    if not trace_steps and not tool_calls:
        return ""

    summary_text = "AI đã kiểm tra dữ liệu trong hệ thống trước khi trả lời."
    if live:
        summary_text = "AI đang kiểm tra dữ liệu và chọn công cụ phù hợp để trả lời."
    elif tool_calls:
        tool_names = ", ".join(tool_call.get("tool", "tool") for tool_call in tool_calls[:3])
        if len(tool_calls) > 3:
            tool_names += ", ..."
        summary_text = f"AI đã dùng {len(tool_calls)} công cụ để kiểm tra dữ liệu: {tool_names}."

    open_attr = " open" if live else ""
    html_parts = [
        '<div class="agent-trace-shell">',
        f'<details class="agent-trace-disclosure"{open_attr}>',
        '<summary class="agent-trace-summary">',
        '<div class="agent-trace-summary-main">',
        '<div class="agent-trace-kicker">AI kiểm tra dữ liệu</div>',
        f'<div class="agent-trace-summary-text">{html.escape(summary_text)}</div>',
        '</div>',
        '<div class="agent-trace-summary-meta">',
        f'<span class="agent-trace-chip">{len(trace_steps)} bước</span>',
        f'<span class="agent-trace-chip">{len(tool_calls)} tool</span>',
    ]

    if live:
        html_parts.append('<div class="agent-trace-live">Đang cập nhật</div>')

    html_parts.extend([
        '</div>',
        '</summary>',
        '<div class="agent-trace-panel">',
    ])

    if trace_steps:
        html_parts.append('<div class="agent-trace-steps-inline">')
        for index, step in enumerate(trace_steps, start=1):
            kind = html.escape(step.get("kind", "thinking"))
            label = html.escape(TRACE_KIND_LABELS.get(step.get("kind", "thinking"), "Bước"))
            html_parts.extend([
                '<div class="agent-trace-pill">',
                f'<span class="agent-trace-pill-dot agent-trace-dot-{kind}"></span>',
                f'<span>{index}. {label}</span>',
                '</div>',
            ])
        html_parts.append('</div>')

        html_parts.append('<div class="agent-trace-details">')
        for step in trace_steps:
            kind = html.escape(step.get("kind", "thinking"))
            label = html.escape(TRACE_KIND_LABELS.get(step.get("kind", "thinking"), "Bước"))
            title = html.escape(step.get("title", "Đang xử lý"))
            detail = html.escape(step.get("detail", ""))
            html_parts.extend([
                '<div class="agent-trace-step">',
                f'<div class="agent-trace-dot agent-trace-dot-{kind}"></div>',
                '<div>',
                f'<div class="agent-trace-step-title">{label} · {title}</div>',
                f'<div class="agent-trace-step-detail">{detail}</div>',
                '</div>',
                '</div>',
            ])
        html_parts.append('</div>')

    if tool_calls:
        html_parts.append('<div class="agent-trace-tools-label">Tool-call theo từng bước</div>')
        for index, tool_call in enumerate(tool_calls, start=1):
            tool_name = html.escape(tool_call.get("tool", "tool"))
            status = tool_call.get("status", "completed")
            status_label = "Đang chạy" if status == "running" else "Hoàn tất"
            input_text = html.escape(tool_call.get("input", ""))
            output_text = html.escape(tool_call.get("output", ""))
            open_attr = " open" if live or status == "running" else ""

            html_parts.extend([
                f'<details class="agent-tool-card"{open_attr}>',
                '<summary class="agent-tool-summary">',
                f'<span class="agent-tool-name">Bước {index}: {tool_name}</span>',
                f'<span class="agent-tool-status agent-tool-status-{status}">{status_label}</span>',
                '</summary>',
                '<div class="agent-tool-body">',
                '<div class="agent-tool-caption">Input</div>',
                f'<pre class="agent-tool-pre">{input_text}</pre>',
                '<div class="agent-tool-caption">Output</div>',
                f'<pre class="agent-tool-pre">{output_text or "Đang chờ kết quả..."}</pre>',
                '</div>',
                '</details>',
            ])

    html_parts.extend([
        "</div>",
        "</details>",
        "</div>",
    ])
    return "".join(html_parts)


def render_agent_trace(trace_steps, tool_calls, placeholder=None, live=False):
    trace_html = build_agent_trace_html(trace_steps, tool_calls, live=live)
    if not trace_html:
        return

    if placeholder is None:
        st.markdown(trace_html, unsafe_allow_html=True)
    else:
        placeholder.markdown(trace_html, unsafe_allow_html=True)

# Lấy cấu hình LLM từ file .env.
llm_api_key = get_llm_api_key()
llm_display_name = get_llm_display_name()
VIEW_CHAT = "Chat"
VIEW_DASHBOARD = "Tổng quan học tập"
VIEW_TRUST = "Kiểm chứng AI"

def login_page():
    st.title("🏫 Hệ thống Hỗ trợ Phụ huynh")
    st.markdown("Vui lòng đăng nhập để tra cứu thông tin học tập của con (Hỗ trợ 24/7).")
    
    with st.form("login_form"):
        username = st.text_input("Mã phụ huynh hoặc Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập")
        
        if submitted:
            try:
                user_info = authenticate_parent(username, password)
                if user_info:
                    st.session_state["logged_in"] = True
                    st.session_state["parent_info"] = user_info
                    
                    # Fetch mock initial data needed for UI context
                    st.session_state["student_data"] = {"student": get_student_info(user_info["student_id"])}
                    st.session_state["messages"] = []
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không chính xác.")
            except psycopg2.errors.OperationalError:
                st.warning("Hệ thống Database đang khởi động lại (Cold Start) theo chế độ tự động tắt tiết kiệm điền của hệ thống, vui lòng chờ 10-15 giây...")
                st.button("Thử lại")
                st.stop()
            except Exception as e:
                st.error(f"Lỗi hệ thống: {e}")
    
    st.info("💡 Mẹo: Dùng tài khoản mẫu `parentA@example.com` hoặc `PH001` / pass: `123456`")

def render_dashboard_view(student):
    student_id = student.get("student_id")
    st.title("Tổng quan học tập")
    st.caption("Dữ liệu gốc từ PostgreSQL cho học sinh đang đăng nhập.")

    grades = get_grades(student_id)
    attendance = get_attendance(student_id)
    tuition = get_tuition(student_id)
    comments = get_teacher_comments(student_id, limit=5)

    latest_score = "-"
    if grades:
        latest_score = f"{grades[0].get('score')} ({grades[0].get('subject')})"

    absent_or_late = sum(1 for row in attendance if row.get("status") in {"absent", "late", "excused"})
    pending_fees = sum(1 for fee in tuition if fee.get("status") in {"pending", "overdue"})

    col1, col2, col3 = st.columns(3)
    col1.metric("Điểm gần nhất", latest_score)
    col2.metric("Buổi cần chú ý", absent_or_late)
    col3.metric("Khoản phí chờ xử lý", pending_fees)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Điểm số")
        if grades:
            grades_df = pd.DataFrame(grades)
            grades_df["score"] = pd.to_numeric(grades_df["score"])
            grades_display = grades_df[["subject", "type", "score", "updated_at"]].rename(columns={
                "subject": "Môn học",
                "type": "Bài đánh giá",
                "score": "Điểm",
                "updated_at": "Cập nhật lúc",
            })
            st.dataframe(grades_display, use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có dữ liệu điểm.")

    with right:
        st.subheader("Chuyên cần")
        if attendance:
            attendance_df = pd.DataFrame(attendance)
            attendance_display = attendance_df[["date", "status", "updated_at"]].rename(columns={
                "date": "Ngày",
                "status": "Trạng thái",
                "updated_at": "Cập nhật lúc",
            })
            st.dataframe(attendance_display, use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có dữ liệu chuyên cần.")

    st.subheader("Học phí")
    if tuition:
        tuition_df = pd.DataFrame(tuition)
        tuition_display = tuition_df.rename(columns={
            "fee_name": "Khoản phí",
            "amount": "Số tiền",
            "due_date": "Hạn nộp",
            "status": "Trạng thái",
        })
        st.dataframe(tuition_display, use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có dữ liệu học phí.")

    st.subheader("Nhận xét giáo viên gần đây")
    if comments:
        comments_display = pd.DataFrame(comments).rename(columns={
            "date": "Ngày",
            "comment": "Nhận xét",
            "teacher_name": "Giáo viên",
            "subject": "Môn học",
        })
        st.dataframe(comments_display, use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có nhận xét giáo viên.")


def render_trust_log_view(student):
    student_id = student.get("student_id")
    st.title("Kiểm chứng AI")
    st.caption("Lịch sử câu trả lời AI, nguồn dữ liệu đã dùng và trạng thái chuyển xử lý.")

    audit_logs = get_recent_ai_audit_logs(student_id, limit=20)
    if not audit_logs:
        st.info("Chưa có audit log. Hãy hỏi AI một câu trong Chat rồi quay lại đây.")
        return

    audit_df = pd.DataFrame(audit_logs)
    audit_df["sources"] = audit_df["data_sources"].apply(
        lambda value: ", ".join(value) if isinstance(value, list) else str(value)
    )
    audit_df["answer_preview"] = audit_df["answer_text"].fillna("").str.slice(0, 120)
    audit_df["status"] = audit_df["was_escalated"].apply(lambda value: "Đã chuyển xử lý" if value else "Đã trả lời")
    audit_display = audit_df[["created_at", "status", "intent_name", "sources", "question_text", "answer_preview"]].rename(columns={
        "created_at": "Thời điểm",
        "status": "Trạng thái",
        "intent_name": "Intent",
        "sources": "Nguồn/tool",
        "question_text": "Câu hỏi",
        "answer_preview": "Tóm tắt câu trả lời",
    })

    st.dataframe(
        audit_display,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Chi tiết từng câu trả lời")
    for index, log in enumerate(audit_logs, start=1):
        sources = log.get("data_sources")
        if isinstance(sources, list):
            sources_text = ", ".join(sources)
        else:
            sources_text = str(sources)

        title = f"{index}. {log.get('created_at')} | {log.get('intent_name')}"
        with st.expander(title, expanded=index == 1):
            st.markdown(f"**Câu hỏi:** {log.get('question_text')}")
            st.markdown(f"**Nguồn dữ liệu/tool:** `{sources_text}`")
            st.markdown(f"**Trạng thái:** {'Đã chuyển xử lý' if log.get('was_escalated') else 'Đã trả lời'}")
            st.markdown("**Câu trả lời:**")
            st.markdown(log.get("answer_text", ""))


def chat_page():
    parent_name = st.session_state["parent_info"]["parent_name"]
    student = st.session_state["student_data"].get("student", {})
    
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 0.15rem 0 0.8rem;">
                <div style="font-size: 0.78rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;">
                    Hồ sơ
                </div>
                <div style="margin-top: 0.75rem; font-size: 1.02rem; font-weight: 700; color: #0f172a;">
                    {student.get('full_name') or 'Học sinh'}
                </div>
                <div style="margin-top: 0.22rem; color: #475569; font-size: 0.9rem;">
                    {student.get('class_name') or 'Chưa có lớp'}
                </div>
                <div style="margin-top: 0.9rem; padding-top: 0.8rem; border-top: 1px solid rgba(226, 232, 240, 0.9); color: #334155; font-size: 0.9rem;">
                    Phụ huynh: <strong>{parent_name}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if st.button("Đăng xuất"):
            st.session_state["logged_in"] = False
            for key in ["parent_info", "student_data", "messages"]:
                st.session_state[key] = None
            st.session_state["messages"] = []
            st.rerun()

    view = st.radio(
        "Chế độ xem",
        [VIEW_CHAT, VIEW_DASHBOARD, VIEW_TRUST],
        horizontal=True,
        label_visibility="collapsed",
    )
    if view == VIEW_DASHBOARD:
        render_dashboard_view(student)
        return
    if view == VIEW_TRUST:
        render_trust_log_view(student)
        return
            
    st.title("Hỏi đáp trực tuyến")
    st.caption("AI Assistant cung cấp thông tin học tập nhanh chóng.")

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                render_agent_trace(
                    msg.get("trace_steps", []),
                    msg.get("tool_calls", []),
                    live=False
                )
            
    if prompt := st.chat_input("Hỏi AI về khóa học, điểm số, hoặc nhận xét..."):
        if not llm_api_key:
            st.error("Thiếu `LLM_API_KEY` trong file `.env`.")
            return
            
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            trace_placeholder = st.empty()
            message_placeholder = st.empty()
            
            try:
                agent_result = call_langchain_agent(
                    api_key=llm_api_key,
                    query=prompt,
                    session_state=st.session_state,
                    trace_callback=lambda steps, tool_calls, live: render_agent_trace(
                        steps,
                        tool_calls,
                        placeholder=trace_placeholder,
                        live=live
                    )
                )
                response = agent_result["output"]
                trace_steps = agent_result.get("trace_steps", [])
                tool_calls = agent_result.get("tool_calls", [])
                
                render_agent_trace(
                    trace_steps,
                    tool_calls,
                    placeholder=trace_placeholder,
                    live=False
                )
                
                # Mô phỏng hiệu ứng stream text
                full_response = ""
                for chunk in response.split(" "):
                    full_response += chunk + " "
                    time.sleep(0.01)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                    
            except psycopg2.errors.OperationalError:
                 st.warning("Hệ thống Database đang khởi động lại (Cold Start)...")
                 if st.button("Thử lại truy vấn"): st.rerun()
                 return
                
        st.session_state["messages"].append({
            "role": "assistant",
            "content": response,
            "trace_steps": trace_steps,
            "tool_calls": tool_calls
        })

if __name__ == "__main__":
    if st.session_state["logged_in"]:
        chat_page()
    else:
        login_page()
