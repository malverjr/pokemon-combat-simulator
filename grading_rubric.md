# Pokemon Combat Simulator — Grading Rubric

**Total: 10 points (2.5 points per criterion)**

All grading is done from the submitted GitHub repository: code review of `.py` files, checking `requirements.txt`, reading `README.md` for the deployed URL and contributions, and visiting the Streamlit URL.

---

## Criterion 1: API Usage (2.5 points)

**What to check in code:** Search for `requests.get`, `@st.cache_data`, `try`/`except`, and the three endpoint URLs (`/pokemon/`, `/move/`, `/type/`).

| Score | Criteria |
|-------|----------|
| **2.5** | All three endpoints used correctly (`/pokemon/{name}`, `/move/{name}`, `/type/{name}`). API functions decorated with `@st.cache_data`. Error handling for invalid Pokemon names or failed requests (try/except or status code checks). Type effectiveness calculated correctly for dual-type defenders (multiplying per defender type) |
| **2.0** | Pokemon and move endpoints used correctly with proper JSON navigation. Type effectiveness either missing entirely or only handles single-type defenders. Caching present |
| **1.5** | Pokemon endpoint works and data is extracted correctly. Move endpoint has issues (e.g., doesn't filter `power: None` moves, or move data is incomplete). No type effectiveness. Some caching |
| **1.0** | Makes API calls with `requests.get()` and parses JSON with `.json()`, but data extraction is incomplete (e.g., only gets name and sprite, misses stats or moves) |
| **0.5** | Attempts `requests.get()` but response is not properly parsed or used (e.g., prints raw response, doesn't call `.json()`, or hardcodes data alongside API calls) |
| **0.0** | No API usage — data is hardcoded or no requests made |

**Key requirements:** All three endpoints, `@st.cache_data`, error handling, dual-type effectiveness.

---

## Criterion 2: Pandas Usage (2.5 points)

**What to check in code:** Search for `pd.DataFrame`, `.melt(`, and how DataFrames are used in chart creation and `st.dataframe`/`st.table` calls.

| Score | Criteria |
|-------|----------|
| **2.5** | All three required DataFrames implemented: (1) stat comparison DataFrame reshaped with `.melt()` for the grouped bar chart, (2) battle log DataFrame built from list of dicts via `pd.DataFrame(battle_log)`, (3) HP over time DataFrame in tidy format for the line chart |
| **2.0** | Two of the three DataFrames are correct and well-structured. The third is either missing or uses a non-DataFrame approach (e.g., plain lists for the chart) |
| **1.5** | One DataFrame is correctly used (most commonly the battle log). The other two use plain dicts/lists instead of DataFrames, or are present but not properly structured |
| **1.0** | `pd.DataFrame()` is called but the structure is wrong (e.g., wrong columns, data is hardcoded instead of built from API/simulation results) or DataFrame is created but never used in the dashboard |
| **0.0** | No pandas usage |

**Key requirements:** `.melt()` for stat comparison, `pd.DataFrame(battle_log)` for log, tidy format for HP over time.

---

## Criterion 3: Dashboard Quality (2.5 points)

**What to check in code:** Look for the 6 required sections by searching for relevant Streamlit calls: `st.selectbox`/`st.text_input` (selection), `st.image` (sprites), `st.plotly_chart` (charts), `st.button` (battle), `st.dataframe`/`st.table` (log table), and `st.columns` (layout). Also verify by visiting the deployed URL if available.

| Score | Criteria |
|-------|----------|
| **2.5** | All 6 required sections present in code: (1) Pokemon selection widgets, (2) Pokemon display with `st.image` for sprites + name/types/stats, (3) move selection widgets filtering to damaging moves, (4) stat comparison Plotly chart, (5) battle button + battle log table + winner announcement, (6) HP over time Plotly chart. Good layout using `st.columns` for side-by-side Pokemon panels. Error states handled gracefully |
| **2.0** | 5 of 6 sections present in code (typically the HP over time chart is missing). Layout uses columns. Sprites displayed. Winner announced |
| **1.5** | 3-4 sections present. Layout is basic (single column, no visual structure). Some charts or the battle simulation may be incomplete |
| **1.0** | Code shows Pokemon selection and basic display, but most other sections are missing or broken. Minimal interactivity |
| **0.5** | Code exists but would crash on interaction (obvious bugs like undefined variables, missing imports) |
| **0.0** | No working app code submitted |

**Key requirements:** All 6 sections, two-column layout, sprites, battle log table + HP chart in results.

**Positive indicators** (not required, for borderline decisions): effectiveness messages ("Super effective!"), additional visualizations (radar chart for stats), PP tracking, rematch button, move descriptions.

---

## Criterion 4: Repo Structure & Deployment (2.5 points)

**What to check:** Verify the repo contains `requirements.txt` at the root, `README.md` with a Streamlit URL and contributions section. Visit the Streamlit URL to confirm deployment works.

| Score | Criteria |
|-------|----------|
| **2.5** | Public repo with clean structure: `requirements.txt` in root with correct dependencies, `README.md` contains a working Streamlit URL (app is functional when visited) and a contributions section listing each member. Code is well-organized (reasonable file/function structure) |
| **2.0** | Repo structure is correct with `requirements.txt` and `README.md`. Streamlit URL is present but has a minor issue (e.g., a missing dependency causes partial functionality, or the app is slow but works). Contributions section present |
| **1.5** | Repo contains complete code and `requirements.txt`, but either: no Streamlit URL in README, URL is broken/expired, or contributions section is missing |
| **1.0** | Repo exists but is incomplete: `requirements.txt` is missing or has wrong dependencies, no README, or code is disorganized (e.g., everything in one giant function, no structure) |
| **0.0** | No repository submitted |

**Key requirements:** `requirements.txt` in root, `README.md` with working Streamlit URL + contributions, clean repo structure.

---

## Grading Summary Table

| Criterion | Max | What to Check in Repo |
|-----------|-----|----------------------|
| API Usage | 2.5 | Search code for `requests.get`, `@st.cache_data`, `try/except`, three endpoint URLs |
| Pandas Usage | 2.5 | Search code for `pd.DataFrame`, `.melt(`, DataFrame usage in charts/tables |
| Dashboard Quality | 2.5 | Search code for `st.image`, `st.plotly_chart`, `st.button`, `st.columns`, `st.dataframe` |
| Repo & Deployment | 2.5 | Check `requirements.txt`, `README.md` (Streamlit URL + contributions), visit deployed URL |

## General Deductions (applied after per-criterion scoring)

- **-0.2** per criterion: Hardcoded API data instead of fetching dynamically, significant dead/commented-out code
- **-0.1** per criterion: Obvious bugs in code that would crash on valid interactions (e.g., undefined variables, wrong function signatures)

## Academic Integrity

- **Automatic 0 on assignment**: Identical non-trivial code patterns across groups (beyond shared API structure), or evidence of code sharing between groups
