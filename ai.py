import os, json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
def _setting(name, default=None):
    value=os.getenv(name)
    if value: return value
    try: return st.secrets.get(name, default)
    except Exception: return default

MODEL=_setting("OPENAI_MODEL","gpt-5.6")
def client():
    k=_setting("OPENAI_API_KEY")
    if not k or str(k).startswith("your_"):
        raise RuntimeError("OPENAI_API_KEY را در .env یا Streamlit Secrets قرار بده.")
    return OpenAI(api_key=k)

SYS="""You are an expert AI Engineering interview tutor.
Persian content must be natural Persian; use English only for unavoidable technical names and code.
English interview content must be English only, with easy B1-B2 spoken language.
Do not expose chain-of-thought. Give concise reasoning summaries and teaching explanations.
Questions must be specific to the exact topic, non-duplicative, realistic for junior/intern AI/Data interviews."""

def lesson(skill,topic):
    p=f"""Teach {skill} > {topic}.
Return exactly:
<<<FA_SIMPLE>>> very simple Persian explanation for a beginner.
<<<FA_FULL>>> complete Persian lesson: definition, intuition, mechanics, when/why, pitfalls, interview knowledge.
<<<EN_SIMPLE>>> easy English-only explanation.
<<<EXAMPLE>>> practical example in Persian plus small code when useful.
<<<DIAGRAM>>> Valid Mermaid only. Use exactly flowchart LR on the first line. Use only simple English ASCII labels, square brackets, and --> arrows. Maximum 6 nodes. No parentheses, quotes, braces, colons, HTML, markdown fences, or Persian text.
<<<KEY_POINTS>>> 5 key points in Persian."""
    return client().responses.create(model=MODEL,instructions=SYS,input=p).output_text

def questions(skill,topic,level):
    meanings={"essential":"10 fundamental questions the candidate MUST know",
              "recommended":"10 practical/intermediate questions the candidate SHOULD know",
              "advanced":"10 deeper bonus questions for extra knowledge"}
    p=f"""Skill: {skill}
Exact topic: {topic}
Generate {meanings[level]}.
Return ONLY a JSON array of exactly 10 unique English interview-question strings.
Every question must directly test {topic}; avoid generic filler."""
    r=client().responses.create(model=MODEL,instructions=SYS,input=p).output_text
    a=r.find("["); b=r.rfind("]")
    return json.loads(r[a:b+1])

def answer(skill,topic,q):
    p=f"""Skill:{skill}
Topic:{topic}
Question:{q}
Return exactly:
<<<FA_EXPLAIN>>> Explain what the question means and the answer in very simple Persian, then give a slightly deeper Persian explanation and one example.
<<<EN_ANSWER>>> English-only concise B1-B2 interview answer the candidate can say.
<<<TIP>>> Persian interview tip: what is being tested and common mistake."""
    return client().responses.create(model=MODEL,instructions=SYS,input=p).output_text


def tutor_chat(message, skill="", topic="", current_question="", lesson_context="", history=None):
    history=history or []
    instructions=SYS+f"""
You are also the learner's interactive personal tutor.
Current Skill: {skill or 'General'}
Current Topic: {topic or 'General'}
Current interview question: {current_question or 'None'}
Relevant visible material: {lesson_context[:5000] if lesson_context else 'None'}
If the learner writes Persian, answer primarily in simple natural Persian. Keep useful technical terms in English.
If they say they did not understand, explain from zero with a new analogy and concrete example, not the same wording.
Use short code when useful. For interview practice, explain what is tested and give a short answer they can say.
If explicitly asked for an English answer, that requested answer must be English only. Do not expose hidden chain-of-thought.
"""
    conversation=[]
    for item in history[-12:]:
        role=item.get("role","user")
        if role not in ("user","assistant"): role="user"
        conversation.append({"role":role,"content":item.get("content","")})
    conversation.append({"role":"user","content":message})
    return client().responses.create(model=MODEL,instructions=instructions,input=conversation).output_text
