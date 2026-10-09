CSS = """
<style>
    :root {
        --bg-1: #0a0f1d;
        --bg-2: #111827;
        --panel: rgba(17, 24, 39, 0.72);
        --panel-soft: rgba(17, 24, 39, 0.48);
        --line: rgba(148, 163, 184, 0.20);
        --text: #e5eefc;
        --muted: #a7b7d6;
        --primary: #7c3aed;
        --primary-2: #22d3ee;
        --success: #34d399;
        --warning: #fbbf24;
        --danger: #f87171;
    }

    .stApp {
        background: radial-gradient(circle at top left, rgba(124, 58, 237, 0.18), transparent 24%),
                    radial-gradient(circle at bottom right, rgba(34, 211, 238, 0.16), transparent 24%),
                    linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1480px;
    }

    .app-shell {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .brand-card,
    .panel-card,
    .sidebar-panel {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.74), rgba(15, 23, 42, 0.55));
        border: 1px solid var(--line);
        border-radius: 22px;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.22);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }

    .brand-card {
        padding: 1.2rem 1.3rem;
        margin-bottom: 0.35rem;
    }

    .eyebrow {
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--primary-2);
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .big-title {
        font-size: clamp(1.7rem, 2.5vw, 2.8rem);
        line-height: 1.1;
        font-weight: 800;
        color: #f8fbff !important;
        margin: 0;
    }

    .subtitle {
        font-size: 0.92rem;
        color: var(--muted) !important;
        margin-top: 0.45rem;
    }

    .panel-card {
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
    }

    .panel-title {
        font-size: 1.02rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: #f8fbff !important;
        margin: 0;
    }

    .mini-list {
        display: grid;
        gap: 0.4rem;
        margin-top: 0.7rem;
        color: var(--muted);
        font-size: 0.92rem;
    }

    h1, h2, h3, h4, h5, p, label, .stMarkdown {
        color: var(--text) !important;
    }

    .status-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 40px;
        padding: 0.42rem 0.9rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        color: #f8fbff;
        border: 1px solid rgba(255,255,255,0.14);
        background: rgba(255,255,255,0.04);
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
        width: 100%;
    }

    .status-chip.ok {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.22), rgba(16, 185, 129, 0.18));
    }

    .status-chip.warn {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.22), rgba(245, 158, 11, 0.15));
        color: #fef3c7;
    }

    .status-chip.error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.24), rgba(239, 68, 68, 0.18));
    }

    .metric-card {
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.86rem 0.9rem;
        background: rgba(15, 23, 42, 0.56);
        backdrop-filter: blur(14px);
        min-height: 100px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .metric-card .label {
        color: var(--muted);
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 700;
    }

    .metric-card .value {
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 0.38rem;
        color: #f8fbff;
        word-break: break-word;
    }

    .stSidebar {
        background: rgba(15, 23, 42, 0.82);
        border-right: 1px solid var(--line);
        backdrop-filter: blur(18px);
    }

    .sidebar-panel {
        padding: 1rem 0.9rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #4f46e5);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.1rem;
        font-weight: 700;
        box-shadow: 0 16px 30px rgba(124, 58, 237, 0.28);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 18px 32px rgba(124, 58, 237, 0.34);
        background: linear-gradient(135deg, #8b5cf6, #4f46e5);
    }

    .stFileUploader > div {
        background: rgba(15, 23, 42, 0.52);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.4rem;
    }

    .stChatMessage {
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(15, 23, 42, 0.46);
        padding: 0.7rem 0.85rem;
    }

    .stExpander {
        border: 1px solid var(--line);
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.4);
    }

    .stCode {
        background: rgba(2, 6, 23, 0.9) !important;
        border: 1px solid var(--line);
        border-radius: 12px;
        color: #e2e8f0 !important;
    }

    .stSlider > div {
        background: rgba(15, 23, 42, 0.35);
        border-radius: 14px;
        padding: 0.5rem 0.7rem;
    }

    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.45);
    }

    .stAlert {
        border-radius: 14px;
    }

    .stWarning,
    .stError,
    .stInfo,
    .stSuccess {
        border: none;
        border-radius: 14px;
    }

    .stTabs [role="tablist"] {
        gap: 0.5rem;
    }

    .stTabs [role="tab"] {
        border-radius: 10px;
        padding: 0.55rem 0.8rem;
    }
</style>
"""
