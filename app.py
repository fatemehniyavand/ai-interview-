import streamlit as st, json, re, html, io
from datetime import date
from pathlib import Path
from db import done,set_done,note,set_note,cache,set_cache,events_on,completed_dates
from ai import lesson,questions,answer,tutor_chat
try:
    from streamlit_mermaid import st_mermaid
except: st_mermaid=None

st.set_page_config(page_title="AI Interview Academy",page_icon="◈",layout="wide")


st.markdown("""
<style>

/* ===== FORCE AI TUTOR + DIALOG TO LIGHT MODE ===== */

/* Entire dialog/modal */
div[role="dialog"],
div[role="dialog"] > div,
div[role="dialog"] section,
div[data-testid="stDialog"],
div[data-testid="stDialog"] > div {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

/* EVERYTHING inside Tutor must use dark text */
div[role="dialog"] *,
div[data-testid="stDialog"] * {
    color: #111827 !important;
}

/* Tutor textarea */
div[role="dialog"] textarea,
div[data-testid="stDialog"] textarea,
div[role="dialog"] div[data-baseweb="textarea"],
div[data-testid="stDialog"] div[data-baseweb="textarea"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
}

/* Textarea internal wrappers */
div[role="dialog"] div[data-baseweb="textarea"] > div,
div[data-testid="stDialog"] div[data-baseweb="textarea"] > div {
    background-color: #FFFFFF !important;
}

/* Tutor input */
div[role="dialog"] input,
div[data-testid="stDialog"] input {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
}

/* Placeholder */
div[role="dialog"] textarea::placeholder,
div[role="dialog"] input::placeholder,
div[data-testid="stDialog"] textarea::placeholder,
div[data-testid="stDialog"] input::placeholder {
    color: #6B7280 !important;
    -webkit-text-fill-color: #6B7280 !important;
    opacity: 1 !important;
}

/* AI/User chat messages */
div[role="dialog"] [data-testid="stChatMessage"],
div[data-testid="stDialog"] [data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #D7DEE8 !important;
    border-radius: 12px !important;
}

/* Markdown / AI responses */
div[role="dialog"] [data-testid="stMarkdownContainer"],
div[role="dialog"] [data-testid="stMarkdownContainer"] *,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"],
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] * {
    color: #111827 !important;
}

/* Context/info boxes */
div[role="dialog"] [data-testid="stAlert"],
div[data-testid="stDialog"] [data-testid="stAlert"] {
    background-color: #F4F7FB !important;
    color: #111827 !important;
}

div[role="dialog"] [data-testid="stAlert"] *,
div[data-testid="stDialog"] [data-testid="stAlert"] * {
    color: #111827 !important;
}

/* Buttons */
div[role="dialog"] button,
div[data-testid="stDialog"] button {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1.5px solid #B8C5D6 !important;
}

div[role="dialog"] button *,
div[data-testid="stDialog"] button * {
    color: #111827 !important;
}

div[role="dialog"] button:hover,
div[data-testid="stDialog"] button:hover {
    background-color: #EEF4FF !important;
    color: #111827 !important;
    border-color: #2563EB !important;
}

/* Code shown by AI */
div[role="dialog"] pre,
div[role="dialog"] code,
div[data-testid="stDialog"] pre,
div[data-testid="stDialog"] code {
    background-color: #F8FAFC !important;
    color: #111827 !important;
}

/* Dialog close button */
div[role="dialog"] button[aria-label="Close"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

/* ===== END TUTOR LIGHT MODE ===== */

</style>
""", unsafe_allow_html=True)




# ===== GLOBAL WHITE UI START =====
st.markdown("""
<style>

/* =========================================
   GLOBAL: WHITE BACKGROUND + DARK TEXT
   ========================================= */

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
.main .block-container {
    background: #FFFFFF !important;
    color: #111827 !important;
}

/* Normal Streamlit text */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] h5,
[data-testid="stAppViewContainer"] h6 {
    color: #111827;
}

/* -----------------------------------------
   USER INPUTS
   ----------------------------------------- */

input,
textarea,
div[data-baseweb="input"],
div[data-baseweb="textarea"],
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    opacity: 1 !important;
}

input::placeholder,
textarea::placeholder {
    color: #6B7280 !important;
    -webkit-text-fill-color: #6B7280 !important;
    opacity: 1 !important;
}

/* -----------------------------------------
   AI CHAT — USER + ASSISTANT
   ----------------------------------------- */

[data-testid="stChatMessage"],
[data-testid="stChatMessageContent"],
div[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    color: #111827 !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em {
    color: #111827 !important;
}

/* Chat input */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* -----------------------------------------
   MARKDOWN / AI ANSWERS / LESSONS
   ----------------------------------------- */

[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em {
    color: #111827 !important;
}

/* -----------------------------------------
   EXPANDERS
   ----------------------------------------- */

[data-testid="stExpander"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    background: #FFFFFF !important;
    color: #111827 !important;
}

/* -----------------------------------------
   SELECTBOX / MULTISELECT
   ----------------------------------------- */

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #111827 !important;
}

div[data-baseweb="select"] span {
    color: #111827 !important;
}

/* Dropdown menu */
div[role="listbox"],
div[role="option"] {
    background: #FFFFFF !important;
    color: #111827 !important;
}

/* -----------------------------------------
   BUTTONS
   ----------------------------------------- */

.stButton > button,
.stDownloadButton > button,
button[kind="secondary"],
button[kind="primary"] {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1.5px solid #B8C5D6 !important;
    font-weight: 700 !important;
}

.stButton > button *,
.stDownloadButton > button * {
    color: #111827 !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #EEF4FF !important;
    color: #111827 !important;
    border-color: #2563EB !important;
}

/* -----------------------------------------
   CODE BLOCKS
   ----------------------------------------- */

[data-testid="stCodeBlock"],
[data-testid="stCodeBlock"] pre,
[data-testid="stCodeBlock"] code {
    background: #FFFFFF !important;
    color: #111827 !important;
}

/* Inline code */
code {
    color: #111827 !important;
}

/* -----------------------------------------
   TABLES / DATAFRAMES
   ----------------------------------------- */

[data-testid="stTable"],
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    color: #111827 !important;
}

/* -----------------------------------------
   ALERTS / INFO / SUCCESS / WARNING
   ----------------------------------------- */

[data-testid="stAlert"] {
    color: #111827 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: #111827 !important;
}

/* -----------------------------------------
   DIALOG — AI TUTOR
   ----------------------------------------- */

div[role="dialog"],
div[role="dialog"] > div,
div[data-testid="stDialog"] {
    background: #FFFFFF !important;
    color: #111827 !important;
}

div[role="dialog"] p,
div[role="dialog"] span,
div[role="dialog"] label,
div[role="dialog"] h1,
div[role="dialog"] h2,
div[role="dialog"] h3 {
    color: #111827 !important;
}

/* -----------------------------------------
   SIDEBAR
   ----------------------------------------- */

[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background: #FFFFFF !important;
    color: #111827 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #111827 !important;
}

/* -----------------------------------------
   CHECKBOX / RADIO
   ----------------------------------------- */

[data-testid="stCheckbox"] label,
[data-testid="stRadio"] label {
    color: #111827 !important;
}

/* Links remain identifiable */
a {
    color: #174EA6 !important;
}

</style>
""", unsafe_allow_html=True)
# ===== GLOBAL WHITE UI END =====


D=json.loads(Path("curriculum.json").read_text(encoding="utf-8"))
V=json.loads(Path("vocabulary.json").read_text(encoding="utf-8"))

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Vazirmatn:wght@400;500;600;700;800&display=swap');
:root{--nav:#0d1b2d;--blue:#2563eb;--ink:#14243b;--muted:#65758b;--line:#dbe3ee;--bg:#f5f7fb;--green:#16834b}
html,body,[class*="css"]{font-family:Inter,Vazirmatn,sans-serif}
.stApp{background:var(--bg);color:var(--ink)}
.block-container{max-width:1500px;padding:1.5rem 2rem 4rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#091727,#132943)}
[data-testid="stSidebar"] *{color:#f4f8ff!important}
h1,h2,h3,h4,p,label,span{color:var(--ink)}
[data-testid="stMetric"]{background:white;border:1px solid var(--line);border-radius:15px;padding:14px}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:#14243b!important}
div[data-testid="stExpander"]{background:white;border:1px solid var(--line);border-radius:13px;overflow:hidden}
div[data-testid="stExpander"] summary{background:#fff;color:#14243b!important}
div[data-testid="stExpander"] summary *{color:#14243b!important}
.stButton button{border-radius:10px;font-weight:700;min-height:46px}
.hero{background:white;border:1px solid var(--line);border-radius:20px;padding:24px 27px;margin-bottom:18px;box-shadow:0 6px 24px rgba(18,36,59,.04)}
.hero h1{font:800 2rem Inter;margin:0;color:#10223a}.hero p{color:var(--muted);margin:.4rem 0 0}
.crumb{font:700 .82rem Inter;color:#2563eb;margin-bottom:9px}
.fa{direction:rtl;text-align:right;font-family:Vazirmatn;background:#fff;border:1px solid var(--line);border-right:4px solid #2563eb;border-radius:14px;padding:17px 19px;line-height:2;margin:10px 0;color:#172a42}
.en{direction:ltr;text-align:left;font-family:Inter;background:#fff;border:1px solid var(--line);border-left:4px solid #0f8a83;border-radius:14px;padding:17px 19px;line-height:1.75;margin:10px 0;color:#172a42}
.topic{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:7px 0}
.word{background:#fff;border:1px solid var(--line);border-radius:12px;padding:11px 13px;margin:5px 0;color:#172a42}
.badge{display:inline-block;padding:4px 9px;border-radius:999px;background:#eaf7ef;color:#13723f;font-size:.75rem;font-weight:800}
.level1{border-left:5px solid #16a34a}.level2{border-left:5px solid #f59e0b}.level3{border-left:5px solid #7c3aed}

/* ===== GLOBAL ACCESSIBILITY / VISIBILITY FIXES ===== */
.stButton > button,
.stDownloadButton > button,
button[kind="secondary"],
button[kind="primary"]{
    background:#ffffff !important;
    color:#13253d !important;
    border:1.5px solid #b9c7d8 !important;
    box-shadow:0 2px 7px rgba(15,35,58,.06) !important;
    min-height:46px !important;
    transition:none !important;
    font-family:Inter,Vazirmatn,sans-serif !important;
    font-weight:700 !important;
}
.stButton > button *,
.stDownloadButton > button *,
button[kind="secondary"] *,
button[kind="primary"] *{
    color:#13253d !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
button[kind="secondary"]:hover,
button[kind="primary"]:hover{
    background:#eaf2ff !important;
    color:#174ea6 !important;
    border-color:#4f7fd8 !important;
}
.stButton > button:hover *,
.stDownloadButton > button:hover *{
    color:#174ea6 !important;
}
.stButton > button:focus{
    box-shadow:0 0 0 3px rgba(37,99,235,.16) !important;
}
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input{
    background:#ffffff !important;
    color:#172a42 !important;
    border:1.5px solid #c8d3e1 !important;
    caret-color:#172a42 !important;
}
[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder{
    color:#7b899a !important;
    opacity:1 !important;
}
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] label *{
    color:#172a42 !important;
}
[data-testid="stAlert"] *,
.stCaptionContainer,
.stCaptionContainer *{
    color:#53657b !important;
}
[data-testid="stProgress"] > div{
    background:#e2e8f0 !important;
}

</style>""",unsafe_allow_html=True)

def parse(x):
    out={}
    for t in ["FA_SIMPLE","FA_FULL","EN_SIMPLE","EXAMPLE","DIAGRAM","KEY_POINTS","FA_EXPLAIN","EN_ANSWER","TIP"]:
        m=re.search(rf"<<<{t}>>>\s*(.*?)(?=<<<[A-Z_]+>>>|$)",x,re.S)
        if m: out[t]=m.group(1).strip()
    return out
def card(title,txt,eng=False):
    cls="en" if eng else "fa"
    st.markdown(f'<div class="{cls}"><b>{html.escape(title)}</b><br>{html.escape(txt).replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)

def clean_mermaid(raw):
    """Keep only a small, safe Mermaid flowchart subset to avoid giant syntax-error panels."""
    if not raw: return ""
    x=raw.strip().replace("```mermaid","").replace("```","").strip()
    x=x.replace("\\n","\n")
    lines=[ln.strip() for ln in x.splitlines() if ln.strip()]
    # Find/force a valid flowchart header.
    body=[]
    for ln in lines:
        if ln.lower().startswith(("flowchart ","graph ")):
            continue
        # Allow only basic nodes/arrows. Remove characters that often break Mermaid labels.
        ln=re.sub(r'[\u0600-\u06FF]', '', ln)
        ln=ln.replace('"',"'")
        if "-->" in ln or "---" in ln:
            body.append(ln)
    if not body:
        return "flowchart LR\nA[Concept] --> B[How it works] --> C[Practical use]"
    return "flowchart LR\n" + "\n".join(body[:8])

def render_diagram(raw):
    code=clean_mermaid(raw)
    if st_mermaid:
        try:
            st_mermaid(code,height="260px")
            return
        except Exception:
            pass
    st.markdown(
        '<div class="topic"><b>Visual flow</b><br>'
        'Concept &nbsp; → &nbsp; How it works &nbsp; → &nbsp; Practical use'
        '</div>', unsafe_allow_html=True
    )

def _short_answer(text):
    sec=parse(text or "")
    return sec.get("EN_ANSWER") or sec.get("FA_EXPLAIN") or "Answer not generated yet."

def daily_rows(day):
    rows=[]
    for ev in events_on(day):
        k=ev["item_key"]
        parts=k.split("::")
        row={"Time":ev["completed_at"][11:16],"Type":"Item","Skill":"","Topic":"","Question / Item":k,"Answer summary":""}
        if parts[0]=="q" and len(parts)>=6:
            _,skill,topic,level,num=parts[:5] if len(parts)==5 else parts[:5]
        # Keys contain :: and topic names safely; parse by known layout.
        if k.startswith("q::"):
            pp=k.split("::")
            if len(pp)>=5:
                skill,topic,level,num=pp[1],pp[2],pp[3],pp[4]
                raw=cache(f"qs::{skill}::{topic}::{level}")
                try: qs=json.loads(raw) if raw else []
                except: qs=[]
                idx=int(num)-1 if str(num).isdigit() else -1
                q=qs[idx] if 0<=idx<len(qs) else f"Question {num}"
                row.update({"Type":"Question","Skill":skill,"Topic":topic,"Question / Item":q,"Answer summary":_short_answer(cache("answer::"+k))})
        elif k.startswith("topic::"):
            pp=k.split("::",2)
            if len(pp)==3: row.update({"Type":"Topic","Skill":pp[1],"Topic":pp[2],"Question / Item":"Topic completed"})
        elif k.startswith("vocab::"):
            pp=k.split("::")
            if len(pp)>=3:
                skill=pp[1]; idx=int(pp[2])-1 if pp[2].isdigit() else -1
                words=V.get(skill,[]); label=words[idx][0]+" — "+words[idx][1] if 0<=idx<len(words) else "Vocabulary"
                row.update({"Type":"Vocabulary","Skill":skill,"Question / Item":label})
        rows.append(row)
    return rows

def make_daily_pdf(day, rows):
    # Portable PDF: English question + concise English interview answer.
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_LEFT
    buf=io.BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=34,leftMargin=34,topMargin=34,bottomMargin=34)
    styles=getSampleStyleSheet()
    title=ParagraphStyle('Title2',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=19,leading=23,textColor=colors.HexColor('#14243b'))
    h=ParagraphStyle('H',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=11,leading=14,textColor=colors.HexColor('#174ea6'))
    body=ParagraphStyle('B',parent=styles['BodyText'],fontName='Helvetica',fontSize=9.5,leading=14,textColor=colors.HexColor('#26384d'),alignment=TA_LEFT)
    story=[Paragraph('AI Interview Academy - Daily Review',title),Paragraph(str(day),body),Spacer(1,14)]
    summary=[["Completed items",str(len(rows))],["Questions",str(sum(r['Type']=='Question' for r in rows))],["Topics",str(sum(r['Type']=='Topic' for r in rows))],["Vocabulary",str(sum(r['Type']=='Vocabulary' for r in rows))]]
    tb=Table(summary,colWidths=[130,80]); tb.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor('#eef4ff')),('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#14243b')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#cbd7e6')),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('PADDING',(0,0),(-1,-1),7)])); story += [tb,Spacer(1,18)]
    qrows=[r for r in rows if r['Type']=='Question']
    if qrows:
        story.append(Paragraph('Questions and answer summaries',h)); story.append(Spacer(1,6))
        for i,r in enumerate(qrows,1):
            story.append(Paragraph(f"{i}. {html.escape(r['Question / Item'])}",h))
            story.append(Paragraph(f"{html.escape(r['Skill'])} / {html.escape(r['Topic'])}",body))
            ans=re.sub(r'[^\\x00-\\x7F]+',' ',r['Answer summary'])
            story.append(Paragraph(html.escape(ans[:1400]),body)); story.append(Spacer(1,10))
    else: story.append(Paragraph('No completed interview questions on this date.',body))
    doc.build(story); buf.seek(0); return buf.getvalue()

def skobj(name): return next(x for x in D if x["skill"]==name)

# hierarchical navigation state
for k,v in {"skill":None,"topic":None,"mode":None}.items():
    if k not in st.session_state: st.session_state[k]=v
if "tutor_open" not in st.session_state: st.session_state.tutor_open=False
if "tutor_history" not in st.session_state: st.session_state.tutor_history=[]
if "tutor_question" not in st.session_state: st.session_state.tutor_question=""
if "tutor_context_text" not in st.session_state: st.session_state.tutor_context_text=""
if "daily_view" not in st.session_state: st.session_state.daily_view=False
def open_tutor(question="",context_text=""):
    st.session_state.tutor_open=True
    st.session_state.tutor_question=question
    st.session_state.tutor_context_text=context_text



@st.dialog("💬 AI Tutor", width="large")
def tutor_dialog():
    skill_ctx=st.session_state.get("skill") or ""
    topic_ctx=st.session_state.get("topic") or ""
    question_ctx=st.session_state.get("tutor_question") or ""
    lesson_ctx=st.session_state.get("tutor_context_text") or ""

    st.caption("هر چیزی را نفهمیدی همین‌جا بپرس؛ این پنجره روی همان صفحه باز می‌ماند.")
    bits=[]
    if skill_ctx: bits.append("Skill: "+skill_ctx)
    if topic_ctx: bits.append("Topic: "+topic_ctx)
    if question_ctx: bits.append("Question: "+question_ctx)
    if bits: st.info("Context فعلی → "+" • ".join(bits))
    else: st.info("سؤال آزاد درباره AI، Data Science، Computer Science یا مصاحبه")

    chat_box=st.container(height=330,border=True)
    with chat_box:
        if not st.session_state.tutor_history:
            st.markdown("**🤖 AI Tutor:** سؤالت را پایین بنویس. می‌توانی بگویی «نفهمیدم»، «ساده‌تر بگو»، «مثال بزن» یا «جواب مصاحبه بده».")
        for msg in st.session_state.tutor_history:
            if msg["role"]=="user":
                st.markdown("**🧑‍🎓 من:**")
            else:
                st.markdown("**🤖 AI Tutor:**")
            st.write(msg["content"])

    with st.form("tutor_form",clear_on_submit=True):
        q=st.text_area(
            "سؤالت را اینجا بنویس",
            height=120,
            placeholder="مثلاً: polymorphism را نفهمیدم؛ خیلی ساده و با مثال توضیح بده."
        )
        sent=st.form_submit_button("➤ ارسال به AI",type="primary",use_container_width=True)

    a,b,c=st.columns(3)
    simple=a.button("ساده‌تر توضیح بده",key="dlg_simple",use_container_width=True)
    example=b.button("مثال عملی بزن",key="dlg_example",use_container_width=True)
    interview=c.button("جواب مصاحبه بده",key="dlg_interview",use_container_width=True)

    preset=None
    if simple: preset="این موضوع را نفهمیدم. از صفر، خیلی ساده، با تشبیه و مثال توضیح بده."
    elif example: preset="برای همین موضوع یک مثال عملی و قابل فهم بزن؛ اگر مناسب است کد کوتاه هم بده."
    elif interview: preset="این موضوع را برای مصاحبه توضیح بده و در پایان یک جواب کوتاه English بده که بتوانم در مصاحبه بگویم."
    ask=(q.strip() if sent and q.strip() else preset)

    if sent and not q.strip(): st.warning("اول سؤالت را بنویس.")
    if ask:
        old=st.session_state.tutor_history[:]
        with st.spinner("AI Tutor در حال پاسخ دادن است..."):
            try:
                reply=tutor_chat(ask,skill_ctx,topic_ctx,question_ctx,lesson_ctx,old)
                st.session_state.tutor_history += [
                    {"role":"user","content":ask},
                    {"role":"assistant","content":reply}
                ]
                st.rerun()
            except Exception as e:
                st.error("خطای API: "+str(e))

    x,y=st.columns(2)
    if x.button("🧹 پاک کردن چت",key="dlg_clear",use_container_width=True):
        st.session_state.tutor_history=[]
        st.rerun()
    if y.button("✕ بستن",key="dlg_close",use_container_width=True):
        st.session_state.tutor_open=False
        st.rerun()

with st.sidebar:
    st.markdown("## ◈ AI Interview Academy")
    st.caption("Learn → Practice → Interview")
    if st.button("🏠 Roadmap",use_container_width=True):
        st.session_state.skill=st.session_state.topic=st.session_state.mode=None; st.session_state.daily_view=False; st.rerun()
    if st.button("📅 Daily Review",key="daily_review",use_container_width=True):
        st.session_state.daily_view=True; st.session_state.skill=None; st.session_state.topic=None; st.session_state.mode=None; st.rerun()
    st.markdown("---")
    if st.button("💬 از AI بپرس",key="global_ai",use_container_width=True):
        st.session_state.tutor_open=not st.session_state.tutor_open; st.rerun()
    st.caption("سؤال آزاد • توضیح ساده‌تر • مثال • تمرین مصاحبه")
    st.markdown("---")
    st.caption("LEARNING PATH")
    for s in D:
        label=("✓ " if all(done(f'topic::{s["skill"]}::{t["name"]}') for t in s["topics"]) else "○ ")+s["skill"]
        if st.button(label,key="side"+s["skill"],use_container_width=True):
            st.session_state.daily_view=False; st.session_state.skill=s["skill"]; st.session_state.topic=None; st.session_state.mode=None; st.rerun()

st.markdown('<div class="hero"><h1>AI Interview Academy</h1><p>One roadmap. One skill at a time. Learn it, practice it, master the interview.</p></div>',unsafe_allow_html=True)

# DAILY REVIEW / CALENDAR
if st.session_state.daily_view:
    st.markdown("## 📅 Daily Review & Study Calendar")
    st.caption("هر تیکی که می‌زنی با تاریخ همان روز ذخیره می‌شود. یک روز را از تقویم انتخاب کن تا کارهای انجام‌شده و سؤال‌وجواب‌هایش را ببینی.")
    counts=completed_dates()
    c1,c2,c3=st.columns([1,1,1])
    selected=c1.date_input("روز موردنظر",value=date.today())
    rows=daily_rows(selected)
    c2.metric("Completed",len(rows))
    c3.metric("Interview questions",sum(r["Type"]=="Question" for r in rows))
    if counts:
        recent=sorted(counts.items(),reverse=True)[:14]
        st.markdown("### روزهای فعال اخیر")
        st.markdown(" ".join([f'<span class="badge">{d}: {n}</span>' for d,n in recent]),unsafe_allow_html=True)
    st.markdown("### جدول فعالیت‌های این روز")
    if rows:
        st.dataframe(rows,use_container_width=True,hide_index=True,column_order=["Time","Type","Skill","Topic","Question / Item","Answer summary"])
        pdf=make_daily_pdf(selected,rows)
        st.download_button("⬇️ دانلود PDF خلاصه امروز",data=pdf,file_name=f"AI_Interview_Daily_{selected}.pdf",mime="application/pdf",use_container_width=True)
    else:
        st.info("برای این روز هنوز موردی ثبت نشده است.")

# ROADMAP
elif not st.session_state.skill:
    st.markdown("## Learning Roadmap")
    st.caption("از پایه شروع کن و به ترتیب تا AI System Design جلو برو.")
    cols=st.columns(3)
    for idx,s in enumerate(D):
        total=len(s["topics"]); learned=sum(done(f'topic::{s["skill"]}::{t["name"]}') for t in s["topics"])
        with cols[idx%3]:
            st.markdown(f'<div class="topic"><b>{s["order"]:02d}. {html.escape(s["skill"])}</b><br><small>{learned}/{total} topics completed</small></div>',unsafe_allow_html=True)
            st.progress(learned/total if total else 0)
            if st.button("Open skill →",key="open"+s["skill"],use_container_width=True):
                st.session_state.daily_view=False; st.session_state.skill=s["skill"]; st.rerun()

# SKILL PAGE
elif not st.session_state.topic:
    s=skobj(st.session_state.skill)
    st.markdown(f'<div class="crumb">ROADMAP  /  {html.escape(s["skill"])}</div>',unsafe_allow_html=True)
    st.markdown(f"## {s['skill']}")
    st.caption("اول یکی از مباحث را انتخاب کن. داخل هر مبحث آموزش، سؤال و واژگان را خواهی داشت.")
    for t in s["topics"]:
        k=f'topic::{s["skill"]}::{t["name"]}'; learned=done(k)
        c1,c2,c3=st.columns([.08,.72,.20])
        with c1: st.markdown("### ✓" if learned else "### ○")
        with c2:
            st.markdown(f"**{t['order']:02d}. {t['name']}**")
            st.caption("Learning • 30 interview questions • Vocabulary")
        with c3:
            if st.button("Open",key="topic"+k,use_container_width=True):
                st.session_state.topic=t["name"]; st.session_state.mode=None; st.rerun()
        st.divider()

# TOPIC HUB
elif not st.session_state.mode:
    s=skobj(st.session_state.skill); t=next(x for x in s["topics"] if x["name"]==st.session_state.topic)
    st.markdown(f'<div class="crumb">ROADMAP / {html.escape(s["skill"])} / {html.escape(t["name"])}</div>',unsafe_allow_html=True)
    st.markdown(f"## {t['name']}")
    k=f'topic::{s["skill"]}::{t["name"]}'
    v=st.checkbox("✓ این مبحث را یاد گرفتم",value=done(k))
    if v!=done(k): set_done(k,v); st.rerun()
    a,b,c=st.columns(3)
    with a:
        st.markdown("### 📘 آموزش")
        st.write("درس کامل فارسی، توضیح خیلی ساده، English explanation، مثال و نمودار.")
        if st.button("شروع آموزش",use_container_width=True): st.session_state.mode="learn"; st.rerun()
    with b:
        st.markdown("### 🎯 سوالات مصاحبه")
        st.write("۱۰ سؤال اساسی + ۱۰ سؤال پیشنهادی + ۱۰ سؤال تکمیلی، مخصوص همین مبحث.")
        if st.button("مشاهده سوالات",use_container_width=True): st.session_state.mode="questions"; st.rerun()
    with c:
        st.markdown("### Aa واژگان")
        st.write("۵۰ کلمه مرتبط با Skill برای مصاحبه همراه معنی فارسی.")
        if st.button("مشاهده ۵۰ واژه",use_container_width=True): st.session_state.mode="vocab"; st.rerun()
    st.markdown("### یادداشت این مبحث")
    nk=f'note::topic::{s["skill"]}::{t["name"]}'
    nv=st.text_area("note",value=note(nk),height=120,label_visibility="collapsed",placeholder="یادداشت شخصی خودت را اینجا بنویس...")
    if st.button("ذخیره یادداشت"): set_note(nk,nv); st.success("ذخیره شد.")

else:
    s=skobj(st.session_state.skill); t=next(x for x in s["topics"] if x["name"]==st.session_state.topic)
    st.markdown(f'<div class="crumb">ROADMAP / {html.escape(s["skill"])} / {html.escape(t["name"])} / {st.session_state.mode.upper()}</div>',unsafe_allow_html=True)
    if st.button("← برگشت به مبحث"): st.session_state.mode=None; st.rerun()

    if st.session_state.mode=="learn":
        st.markdown(f"## آموزش: {t['name']}")
        ck=f'lesson::{s["skill"]}::{t["name"]}'; txt=cache(ck)
        if not txt and st.button("ساخت درس کامل با AI",type="primary"):
            with st.spinner("در حال ساخت درس..."):
                try: txt=lesson(s["skill"],t["name"]); set_cache(ck,txt)
                except Exception as e: st.error(str(e))
        if txt:
            sec=parse(txt)
            if sec.get("FA_SIMPLE"): card("توضیح خیلی ساده فارسی",sec["FA_SIMPLE"])
            if sec.get("FA_FULL"): card("آموزش کامل فارسی",sec["FA_FULL"])
            if sec.get("EN_SIMPLE"): card("SIMPLE ENGLISH EXPLANATION",sec["EN_SIMPLE"],True)
            if sec.get("EXAMPLE"): card("مثال عملی",sec["EXAMPLE"])
            if sec.get("DIAGRAM"):
                st.markdown("### نمودار مفهومی")
                render_diagram(sec["DIAGRAM"])
            if sec.get("KEY_POINTS"): card("نکات کلیدی",sec["KEY_POINTS"])
            if st.button("💬 این درس را نفهمیدم / از AI بپرس",key="ask_lesson",use_container_width=True):
                open_tutor(context_text=txt); st.rerun()
        nk=f'note::learn::{s["skill"]}::{t["name"]}'
        nv=st.text_area("یادداشت من",value=note(nk),height=110)
        if st.button("ذخیره",key="savelearn"): set_note(nk,nv); st.success("ذخیره شد.")

    elif st.session_state.mode=="vocab":
        st.markdown(f"## 50 Interview Words — {s['skill']}")
        words=V[s["skill"]]
        cols=st.columns(2)
        for i,(w,m) in enumerate(words,1):
            with cols[(i-1)%2]:
                vk=f'vocab::{s["skill"]}::{i}'
                checked=st.checkbox(f"{i:02d}. {w} — {m}",value=done(vk),key=vk)
                if checked!=done(vk): set_done(vk,checked); st.rerun()

    elif st.session_state.mode=="questions":
        st.markdown(f"## سوالات مصاحبه: {t['name']}")
        levels=[("essential","🟢 سوالات اساسی — حتماً باید بلد باشم","level1"),
                ("recommended","🟠 سوالاتی که بهتر است بلد باشم","level2"),
                ("advanced","🟣 سوالات تکمیلی — اطلاعات بیشتر","level3")]
        for lv,title,css in levels:
            st.markdown(f"### {title}")
            qcache=f'qs::{s["skill"]}::{t["name"]}::{lv}'
            raw=cache(qcache); qs=json.loads(raw) if raw else []
            if not qs:
                if st.button(f"ساخت و ذخیره ۱۰ سؤال + پاسخ {title}",key="mk"+qcache):
                    with st.spinner("در حال ساخت سوال‌های مرتبط..."):
                        try:
                            qs=questions(s["skill"],t["name"],lv)
                            set_cache(qcache,json.dumps(qs,ensure_ascii=False))
                            prog=st.progress(0,text="سؤال‌ها ذخیره شدند؛ در حال ساخت و ذخیره پاسخ‌ها...")
                            for qi,qq in enumerate(qs,1):
                                qk2=f'q::{s["skill"]}::{t["name"]}::{lv}::{qi}'
                                ak2="answer::"+qk2
                                if not cache(ak2):
                                    try: set_cache(ak2,answer(s["skill"],t["name"],qq))
                                    except Exception: pass
                                prog.progress(qi/len(qs),text=f"ذخیره پاسخ {qi}/{len(qs)}")
                            st.rerun()
                        except Exception as e: st.error(str(e))
                continue
            for i,q in enumerate(qs,1):
                qk=f'q::{s["skill"]}::{t["name"]}::{lv}::{i}'
                with st.expander(f'{"✓" if done(qk) else "○"} {i:02d}. {q}'):
                    chk=st.checkbox("این سؤال را یاد گرفتم",value=done(qk),key="chk"+qk)
                    if chk!=done(qk): set_done(qk,chk); st.rerun()
                    if st.button("💬 درباره همین سؤال از AI بپرس",key="ask"+qk,use_container_width=True):
                        open_tutor(question=q,context_text=cache("answer::"+qk)); st.rerun()
                    ak="answer::"+qk; at=cache(ak)
                    if not at and st.button("نمایش پاسخ و توضیح",key="ans"+qk,type="primary"):
                        with st.spinner("در حال آماده‌سازی پاسخ..."):
                            try: at=answer(s["skill"],t["name"],q); set_cache(ak,at)
                            except Exception as e: st.error(str(e))
                    if at:
                        sec=parse(at)
                        if sec.get("FA_EXPLAIN"): card("توضیح ساده فارسی + پاسخ",sec["FA_EXPLAIN"])
                        if sec.get("EN_ANSWER"): card("ENGLISH INTERVIEW ANSWER",sec["EN_ANSWER"],True)
                        if sec.get("TIP"): card("نکته مصاحبه",sec["TIP"])
                    nk="note::"+qk
                    nv=st.text_area("یادداشت شخصی این سؤال",value=note(nk),key="nt"+qk,height=90)
                    if st.button("ذخیره یادداشت",key="sv"+qk): set_note(nk,nv); st.success("ذخیره شد.")




# Open the AI Tutor as a real modal dialog on top of the current page.
if st.session_state.get("tutor_open"):
    tutor_dialog()


st.markdown("""
<style>
/* ===== GLOBAL INPUT VISIBILITY FIX ===== */

/* Text inputs */
div[data-testid="stTextInput"] input,
div[data-baseweb="input"] input {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    border-color: #B8C5D6 !important;
    opacity: 1 !important;
}

/* Text areas: Notes + AI Tutor + all multiline fields */
div[data-testid="stTextArea"] textarea,
textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    border-color: #B8C5D6 !important;
    opacity: 1 !important;
}

/* Placeholder */
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder,
input::placeholder,
textarea::placeholder {
    color: #6B7280 !important;
    -webkit-text-fill-color: #6B7280 !important;
    opacity: 1 !important;
}

/* Input wrappers */
div[data-baseweb="input"],
div[data-baseweb="textarea"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

/* Focus */
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border-color: #2563EB !important;
}

/* Number/date inputs */
input[type="number"],
input[type="date"],
input[type="text"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Labels */
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label {
    color: #172A42 !important;
}
</style>
""", unsafe_allow_html=True)
