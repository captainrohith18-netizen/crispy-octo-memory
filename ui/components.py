from __future__ import annotations

import streamlit as st


def render_status_chip(label: str, is_ok: bool = True, warning: bool = False) -> None:
    tone = "ok" if is_ok and not warning else "warn" if warning else "error"
    st.markdown(
        f'<span class="status-chip {tone}">{label}</span>',
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{title}</div>
            <div class="value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
