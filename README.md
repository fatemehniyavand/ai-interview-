# AI Interview Academy V2

Hierarchical flow:
Roadmap → Skill → Topic → Learning / Interview Questions / Vocabulary

Each topic:
- Complete Persian lesson + simple English + example + Mermaid diagram
- 3 interview levels × 10 topic-specific questions
- Persian simple explanation + English interview answer
- Personal note under every question
- Persistent checkboxes, notes, AI lessons and answers in SQLite
- 50 interview vocabulary terms per skill

## macOS
```bash
cd AI_Interview_Academy_V2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```
Edit `.env`, then:
```bash
python -m streamlit run app.py
```

## V3 UI fixes
- All buttons use a light background, dark high-contrast text, visible border, and blue hover state.
- Text areas and inputs are always light with readable dark text.
- Checkbox/caption/metric contrast is normalized.
- Mermaid output is sanitized before rendering, with a clean fallback if generated syntax is invalid.
