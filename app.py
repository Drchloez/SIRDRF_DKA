import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import base64
import os

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return None
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            ext = image_path.split('.')[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{encoded_string}"
    except Exception:
        return None


# ==========================================
# PART 1: OPTIMIZED FUZZY LOGIC FROM SCRATCH
# ==========================================

def triangle_member(x, a, b, c):
    if x <= a or x >= c:
        return 0

    if x == b:
        return 1

    if a < x < b:
        return (x - a) / (b - a)

    if b < x < c:
        return (c - x) / (c - b)

    return 0


def fuzzify_mileage(mileage):
    low = triangle_member(mileage, -40000, 0, 40000)
    medium = triangle_member(mileage, 30000, 50000, 70000)
    high = triangle_member(mileage, 60000, 200000, 400000)
    return {"Low": low, "Medium": medium, "High": high}


def fuzzify_year(year):
    old = triangle_member(year, 2000, 2010, 2018)
    medium = triangle_member(year, 2015, 2018, 2021)
    new = triangle_member(year, 2018, 2023, 2030)
    return {"Old": old, "Medium": medium, "New": new}


def fuzzify_engine(engine_size):
    kecil = triangle_member(engine_size, -1.0, 1.0, 2.0)
    sedang = triangle_member(engine_size, 1.5, 2.5, 3.5)
    besar = triangle_member(engine_size, 3.0, 4.5, 8.0)
    return {"Kecil": kecil, "Sedang": sedang, "Besar": besar}


def fuzzify_mpg(mpg):
    boros = triangle_member(mpg, -20, 20, 40)
    standar = triangle_member(mpg, 30, 50, 70)
    irit = triangle_member(mpg, 60, 70, 120)
    return {"Boros": boros, "Standar": standar, "Irit": irit}


def fuzzify_tax(tax):
    murah = triangle_member(tax, -100, 100, 200)
    standar = triangle_member(tax, 150, 300, 450)
    mahal = triangle_member(tax, 400, 600, 1500)
    return {"Murah": murah, "Standar": standar, "Mahal": mahal}


def rule_evaluation_all(year, mileage, engine_size, mpg, tax):
    year_fuzzy = fuzzify_year(year)
    mileage_fuzzy = fuzzify_mileage(mileage)
    engine_fuzzy = fuzzify_engine(engine_size)
    mpg_fuzzy = fuzzify_mpg(mpg)
    tax_fuzzy = fuzzify_tax(tax)

    rule1 = min(year_fuzzy["New"], mileage_fuzzy["Low"], engine_fuzzy["Besar"])
    rule2 = min(year_fuzzy["Old"], mileage_fuzzy["High"])
    rule3 = min(mpg_fuzzy["Irit"], tax_fuzzy["Murah"])
    rule4 = min(year_fuzzy["New"], mileage_fuzzy["Low"], mpg_fuzzy["Irit"])
    rule5 = min(engine_fuzzy["Besar"], tax_fuzzy["Mahal"])
    rule6 = min(year_fuzzy["Old"], mileage_fuzzy["High"], mpg_fuzzy["Boros"])
    rule7 = min(engine_fuzzy["Kecil"], mpg_fuzzy["Irit"])
    rule8 = min(tax_fuzzy["Mahal"], mileage_fuzzy["Low"])
    rule9 = min(year_fuzzy["Medium"], mileage_fuzzy["Medium"])
    rule10 = min(engine_fuzzy["Kecil"], mileage_fuzzy["High"])
    rule11 = min(year_fuzzy["New"], engine_fuzzy["Besar"])
    rule12 = min(year_fuzzy["Old"], tax_fuzzy["Murah"])
    rule13 = min(mpg_fuzzy["Boros"], tax_fuzzy["Mahal"])
    rule14 = min(mileage_fuzzy["Low"], mpg_fuzzy["Irit"])
    rule15 = min(engine_fuzzy["Sedang"], year_fuzzy["Medium"])
    rule16 = min(year_fuzzy["Medium"], mpg_fuzzy["Standar"])
    rule17 = min(mileage_fuzzy["Medium"], tax_fuzzy["Standar"])
    rule18 = min(engine_fuzzy["Sedang"], mileage_fuzzy["Medium"])
    rule19 = min(year_fuzzy["New"], engine_fuzzy["Sedang"])
    rule20 = min(year_fuzzy["Old"], engine_fuzzy["Kecil"])

    rules_list = [
        rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
        rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20
    ]

    # Optimized rule aggregation dictionary (aligned with optimization)
    agg_dict = {
        "Murah": max(rule2, rule6, rule10, rule12, rule13, rule20),
        "Standar": max(rule3, rule7, rule9, rule15, rule16, rule17),
        "Premium": max(rule4, rule14, rule18, rule19),
        "Mewah": max(rule1, rule5, rule8, rule11)
    }

    return agg_dict, rules_list


def defuzzify_mamdani(output_fuzzy):
    w_murah = output_fuzzy["Murah"]
    w_standar = output_fuzzy["Standar"]
    w_premium = output_fuzzy["Premium"]
    w_mewah = output_fuzzy["Mewah"]

    # Diskritisasi harga dari $0 s.d. $100,000 dengan langkah 500
    y_vals = np.arange(0, 100001, 500)
    numerator = 0
    denominator = 0

    for y in y_vals:
        # Himpunan fuzzy output harga (segitiga) — sinkron dengan notebook
        mu_murah = triangle_member(y, 0, 3500, 15000)
        mu_standar = triangle_member(y, 15000, 23500, 30000)
        mu_premium = triangle_member(y, 26000, 28500, 40000)
        mu_mewah = triangle_member(y, 45000, 75000, 150000)

        mu_y = max(
            min(w_murah, mu_murah),
            min(w_standar, mu_standar),
            min(w_premium, mu_premium),
            min(w_mewah, mu_mewah)
        )

        numerator += y * mu_y
        denominator += mu_y

    if denominator == 0:
        return 0

    return numerator / denominator


def defuzzify_sugeno(rules):
    # Singleton output values per rule — sinkron dengan notebook
    z = [
        75000, 3500, 23500, 28500, 75000, 3500, 23500, 75000, 23500, 3500,
        75000, 3500, 3500, 28500, 23500, 23500, 23500, 28500, 28500, 3500
    ]
    numerator = sum(rules[i] * z[i] for i in range(20))
    denominator = sum(rules)

    if denominator == 0:
        return 0

    return numerator / denominator


def prediksi_harga(year, mileage, engine_size, mpg, tax, method="Mamdani"):
    agg_dict, rules_list = rule_evaluation_all(year, mileage, engine_size, mpg, tax)
    if method.lower() == "sugeno":
        return defuzzify_sugeno(rules_list)
    else:
        return defuzzify_mamdani(agg_dict)


def kategori_mobil(harga):
    if harga < 20000:
        return "Economy"
    if harga < 35000:
        return "Standard"
    if harga < 50000:
        return "Premium"
    return "Luxury"

# ==========================================
# PART 2: STREAMLIT BENTO GRID PAGE SERVING
# ==========================================

def main():
    st.set_page_config(
        page_title="Estimator Harga Mercedes-Benz | Fuzzy Mamdani & Sugeno", 
        page_icon="🚗",
        layout="wide"
    )

    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        [data-testid="stHeader"] {display: none;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            display: block;
            border: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Process the HTML template to inject high-res base64 images
    processed_html = BENTO_GRID_HTML
    
    a_class_url = get_base64_image("assets/a_class.png")
    c_class_url = get_base64_image("assets/c_class.png")
    e_class_url = get_base64_image("assets/e_class.png")
    s_class_url = get_base64_image("assets/s_class.jpg")
    g_class_url = get_base64_image("assets/g_class.jpg")
    sl_class_url = get_base64_image("assets/sl_class.jpg")
    
    if a_class_url:
        processed_html = processed_html.replace('__A_CLASS_URL__', a_class_url)
    if c_class_url:
        processed_html = processed_html.replace('__C_CLASS_URL__', c_class_url)
    if e_class_url:
        processed_html = processed_html.replace('__E_CLASS_URL__', e_class_url)
    if s_class_url:
        processed_html = processed_html.replace('__S_CLASS_URL__', s_class_url)
    if g_class_url:
        processed_html = processed_html.replace('__GLA_URL__', g_class_url)
        processed_html = processed_html.replace('__GLC_URL__', g_class_url)
        processed_html = processed_html.replace('__GLE_URL__', g_class_url)
    if sl_class_url:
        processed_html = processed_html.replace('__SLK_URL__', sl_class_url)
        
    components.html(processed_html, height=970, scrolling=True)

# Self-contained Bento Grid page layout HTML string (CSS & JS injected)
BENTO_GRID_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estimator Harga Mercedes-Benz | Fuzzy Mamdani & Sugeno</title>
    <meta name="description" content="Aplikasi web estimasi harga mobil bekas Mercedes-Benz menggunakan logika fuzzy Mamdani dan Sugeno secara from scratch.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Stylesheet -->
    <style>
/* --- Color Variables & Root Themes --- */
:root {
    --transition-speed: 0.3s;
    --transition-curve: cubic-bezier(0.25, 0.8, 0.25, 1);
}

body.dark-mode {
    --bg-color: #080a10;
    --card-bg: #101422;
    --border-color: #1e253c;
    --text-primary: #ffffff;
    --text-secondary: #94a3b8;
    --accent-color: #00d8f6;
    --accent-bg: rgba(0, 216, 246, 0.1);
    --accent-shadow: rgba(0, 216, 246, 0.25);
    --card-hover-bg: #141b2e;
    --shadow-color: rgba(0, 0, 0, 0.4);
    --header-bg: rgba(8, 10, 16, 0.8);
    --slider-track: #1e253c;
    --input-bg: #161c30;
}

body.light-mode {
    --bg-color: #f8fafc;
    --card-bg: #ffffff;
    --border-color: #e2e8f0;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --accent-color: #0284c7;
    --accent-bg: rgba(2, 132, 199, 0.08);
    --accent-shadow: rgba(2, 132, 199, 0.15);
    --card-hover-bg: #f1f5f9;
    --shadow-color: rgba(15, 23, 42, 0.05);
    --header-bg: rgba(248, 250, 252, 0.8);
    --slider-track: #e2e8f0;
    --input-bg: #f1f5f9;
}

/* --- Base Styles --- */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    transition: background-color var(--transition-speed) var(--transition-curve), 
                border-color var(--transition-speed) var(--transition-curve);
}

body {
    background-color: var(--bg-color);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    padding: 90px 24px 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

h1, h2, h3, .logo-text, .badge, .result-price {
    font-family: 'Outfit', sans-serif;
}

/* --- Header --- */
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 70px;
    background-color: var(--header-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40px;
    border-bottom: 1px solid var(--border-color);
    z-index: 100;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-dot {
    width: 10px;
    height: 10px;
    background-color: var(--accent-color);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--accent-color);
}

.logo-text {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.theme-btn {
    background: none;
    border: 1px solid var(--border-color);
    outline: none;
    cursor: pointer;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    color: var(--text-primary);
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--transition-speed) var(--transition-curve);
}

.theme-btn:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
    box-shadow: 0 0 10px var(--accent-shadow);
}

/* --- Bento Grid Layout --- */
.bento-container {
    max-width: 1200px;
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(185px, auto);
    gap: 20px;
    margin-top: 20px;
}

/* Card Base Styles */
.bento-card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 24px;
    padding: 24px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 4px 20px var(--shadow-color);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.4s var(--transition-curve), 
                box-shadow 0.4s var(--transition-curve), 
                border-color 0.4s var(--transition-curve), 
                background-color 0.4s var(--transition-curve);
}

.bento-card:hover {
    transform: translateY(-6px);
    border-color: var(--accent-color);
    box-shadow: 0 12px 30px -8px var(--accent-shadow);
}

/* Asymmetric Grid Spans */
.card-hero {
    grid-column: span 2;
    grid-row: span 1;
}

.card-info {
    grid-column: span 2;
    grid-row: span 1;
}

.card-input {
    grid-column: span 2;
    grid-row: span 2;
}

.card-visual {
    grid-column: span 2;
    grid-row: span 2;
    padding: 0; /* Full cover container */
}

.card-result {
    grid-column: span 2;
    grid-row: span 1;
}

/* --- Component Customization --- */

/* Hero & Info Cards */
.badge {
    align-self: flex-start;
    padding: 4px 12px;
    background-color: var(--accent-bg);
    color: var(--accent-color);
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
}

.hero-title {
    font-size: 1.6rem;
    font-weight: 800;
    margin: 8px 0;
    line-height: 1.2;
}

.hero-desc, .card-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

.icon-wrap {
    width: 40px;
    height: 40px;
    background-color: var(--accent-bg);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    color: var(--accent-color);
    margin-bottom: 12px;
}

.project-tag {
    font-size: 0.75rem;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-secondary);
    letter-spacing: 1px;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Input Card Form */
.form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 10px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.full-width {
    grid-column: span 2;
}

.form-group label {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-secondary);
}

.select-input {
    background-color: var(--input-bg);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 10px 14px;
    border-radius: 12px;
    font-family: inherit;
    font-size: 0.85rem;
    outline: none;
    cursor: pointer;
    transition: all var(--transition-speed) var(--transition-curve);
}

.select-input:focus {
    border-color: var(--accent-color);
    box-shadow: 0 0 10px var(--accent-shadow);
}

.slider-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.val-bold {
    font-weight: 700;
    color: var(--accent-color);
}

.slider {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: var(--slider-track);
    outline: none;
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--accent-color);
    cursor: pointer;
    box-shadow: 0 0 8px var(--accent-color);
}

.slider::-moz-range-thumb {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--accent-color);
    cursor: pointer;
    box-shadow: 0 0 8px var(--accent-color);
}

.btn-predict {
    width: 100%;
    background-color: var(--accent-color);
    color: #080a10;
    border: none;
    outline: none;
    border-radius: 12px;
    padding: 12px;
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    cursor: pointer;
    margin-top: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all var(--transition-speed) var(--transition-curve);
}

.btn-predict:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--accent-shadow);
}

/* Visual Card */
.visual-wrap {
    position: relative;
    width: 100%;
    height: 100%;
}

.car-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.8s var(--transition-curve);
}

.bento-card:hover .car-img {
    transform: scale(1.05);
}

.visual-overlay {
    position: absolute;
    bottom: 15px;
    left: 15px;
    background: rgba(8, 10, 16, 0.65);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 12px 18px;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    pointer-events: none;
}

body.light-mode .visual-overlay {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(0, 0, 0, 0.08);
}

.model-name {
    font-family: 'Outfit', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
}

/* Results Cards */
.card-result {
    align-items: center;
    justify-content: space-between;
    text-align: center;
}

.result-display {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    margin: 10px 0;
}

.result-price {
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--accent-color);
}

.result-badge {
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 700;
}

.badge-economy { background-color: rgba(34, 197, 94, 0.15); color: #22c55e; }
.badge-standard { background-color: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.badge-premium { background-color: rgba(168, 85, 247, 0.15); color: #a855f7; }
.badge-luxury { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; }

.defuzz-info {
    font-size: 0.7rem;
    color: var(--text-secondary);
}

/* --- Footer --- */
.footer {
    margin-top: 40px;
    padding: 20px 0;
    border-top: 1px solid var(--border-color);
    width: 100%;
    max-width: 1200px;
    text-align: center;
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.footer a {
    color: var(--accent-color);
    text-decoration: none;
    font-weight: 600;
}

/* --- Responsive Media Queries --- */
@media (max-width: 900px) {
    .bento-container {
        grid-template-columns: repeat(2, 1fr);
        grid-auto-rows: minmax(170px, auto);
    }
    
    .card-hero, .card-info, .card-input {
        grid-column: span 2;
    }
    
    .card-visual {
        grid-column: span 2;
        grid-row: span 2;
        min-height: 360px;
    }
    
    .card-result {
        grid-column: span 2;
        grid-row: span 1;
    }
}

@media (max-width: 600px) {
    body {
        padding: 90px 16px 20px;
    }
    
    .header {
        padding: 0 20px;
    }
    
    .bento-container {
        grid-template-columns: 1fr;
        grid-auto-rows: auto;
        gap: 16px;
    }
    
    .card-hero, .card-info, .card-input, .card-visual, .card-result {
        grid-column: span 1;
        grid-row: span 1;
    }
    
    .card-visual {
        min-height: 250px;
    }
    
    .form-grid {
        grid-template-columns: 1fr;
    }
    
    .full-width {
        grid-column: span 1;
    }
    
    .bento-card {
        padding: 20px;
    }
}

</style>
</head>
<body class="dark-mode">

    <!-- Header & Theme Toggle -->
    <header class="header">
        <div class="logo">
            <span class="logo-dot"></span>
            <span class="logo-text">mercedes-fuzzy.ai</span>
        </div>
        <button id="theme-toggle" class="theme-btn" aria-label="Toggle Theme">
            <i class="fa-solid fa-moon"></i>
        </button>
    </header>

    <!-- Bento Grid Container -->
    <main class="bento-container">

        <!-- 1. Header Card (2x1) -->
        <section class="bento-card card-hero" id="hero">
            <div class="hero-details">
                <span class="badge">Dasar Kecerdasan Buatan (DKA)</span>
                <h1 class="hero-title">Estimasi Harga Mercedes-Benz Bekas</h1>
                <p class="hero-desc">
                    Aplikasi cerdas untuk memprediksi harga mobil bekas berdasarkan data riil menggunakan integrasi model Fuzzy Mamdani (Centroid) dan Fuzzy Sugeno Orde Nol tanpa library eksternal.
                </p>
            </div>
        </section>

        <!-- 2. Info / Rules Card (2x1) -->
        <section class="bento-card card-info" id="info">
            <div class="card-header">
                <div class="icon-wrap"><i class="fa-solid fa-circle-info"></i></div>
                <span class="project-tag">Informasi Model</span>
            </div>
            <div class="info-content">
                <h2 class="card-title">Fuzzy Logic from Scratch</h2>
                <p class="card-desc">
                    Sistem ini mengevaluasi <strong>20 aturan inferensi fuzzy</strong> menggunakan input Fuzzifikasi Segitiga. Perbandingan dilakukan antara Mamdani (Center of Area) dan Sugeno (Rata-rata Terbobot) secara langsung di web Anda.
                </p>
            </div>
        </section>

        <!-- 3. Input Data Mobil Card (2x2) -->
        <section class="bento-card card-input" id="input-form">
            <h2 class="card-title"><i class="fa-solid fa-sliders"></i> Input Parameter Mobil</h2>
            
            <div class="form-grid">
                <!-- Dropdown Model -->
                <div class="form-group full-width">
                    <label for="input-model">🚗 Model Mercedes-Benz:</label>
                    <select id="input-model" class="select-input">
                        <option value="A-Class">A-Class (Hatchback)</option>
                        <option value="B-Class">B-Class (MPV)</option>
                        <option value="C-Class" selected>C-Class (Sedan/Coupe)</option>
                        <option value="E-Class">E-Class (Executive Sedan)</option>
                        <option value="S-Class">S-Class (Luxury Sedan)</option>
                        <option value="GLA">GLA (Compact SUV)</option>
                        <option value="GLC">GLC (Premium SUV)</option>
                        <option value="GLE">GLE (Large SUV)</option>
                        <option value="SLK">SLK (Roadster/Convertible)</option>
                        <option value="AMG GT">AMG GT (Supercar)</option>
                    </select>
                </div>

                <!-- Sliders -->
                <div class="form-group">
                    <div class="slider-label">
                        <span>📅 Tahun Mobil:</span>
                        <span id="val-year" class="val-bold">2020</span>
                    </div>
                    <input type="range" id="input-year" min="2010" max="2025" value="2020" class="slider">
                </div>

                <div class="form-group">
                    <div class="slider-label">
                        <span>🛣️ Odometer (Mileage):</span>
                        <span id="val-mileage" class="val-bold">30.000</span>
                    </div>
                    <input type="range" id="input-mileage" min="0" max="200000" step="5000" value="30000" class="slider">
                </div>

                <div class="form-group">
                    <div class="slider-label">
                        <span>⚙️ Kapasitas Mesin:</span>
                        <span id="val-engine" class="val-bold">1.5</span>
                    </div>
                    <input type="range" id="input-engine" min="0.0" max="6.5" step="0.1" value="1.5" class="slider">
                </div>

                <div class="form-group">
                    <div class="slider-label">
                        <span>⛽ MPG (Bahan Bakar):</span>
                        <span id="val-mpg" class="val-bold">40.0</span>
                    </div>
                    <input type="range" id="input-mpg" min="0.0" max="100.0" step="0.1" value="40.0" class="slider">
                </div>

                <div class="form-group full-width">
                    <div class="slider-label">
                        <span>💸 Pajak Tahunan (Tax):</span>
                        <span id="val-tax" class="val-bold">150</span>
                    </div>
                    <input type="range" id="input-tax" min="0" max="1000" step="10" value="150" class="slider">
                </div>
            </div>

            <button id="btn-predict" class="btn-predict" type="button">
                <i class="fa-solid fa-calculator"></i> Hitung Estimasi Harga
            </button>
        </section>

        <!-- 4. Mobil Display Card (1x2) -->
        <section class="bento-card card-visual" id="visual">
            <div class="visual-wrap">
                <img id="car-image" src="__C_CLASS_URL__" alt="Mercedes Model class illustration" class="car-img">
                <div class="visual-overlay">
                    <span id="car-model-name" class="model-name">C-Class</span>
                    <span id="car-class-badge" class="badge">Sedan Class</span>
                </div>
            </div>
        </section>

        <!-- 5. Hasil Mamdani Card (1x1) -->
        <section class="bento-card card-result" id="result-mamdani">
            <div class="card-header">
                <span class="project-tag">Metode Mamdani</span>
                <span class="result-indicator indicator-mamdani">🔴</span>
            </div>
            <div class="result-display">
                <h3 class="result-price" id="price-mamdani">-</h3>
                <span class="result-badge badge-standard" id="badge-mamdani">-</span>
            </div>
            <span class="defuzz-info">Center of Area (COA)</span>
        </section>

        <!-- 6. Hasil Sugeno Card (1x1) -->
        <section class="bento-card card-result" id="result-sugeno">
            <div class="card-header">
                <span class="project-tag">Metode Sugeno</span>
                <span class="result-indicator indicator-sugeno">🟢</span>
            </div>
            <div class="result-display">
                <h3 class="result-price" id="price-sugeno">-</h3>
                <span class="result-badge badge-standard" id="badge-sugeno">-</span>
            </div>
            <span class="defuzz-info">Weighted Average (WA)</span>
        </section>

    </main>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2026 mercedes-fuzzy.ai • Tugas Besar DKA Telkom University • Dataset Source: <a href="https://www.kaggle.com/datasets/koki2525/mercedes-benz-used-car-dataset" target="_blank">Kaggle</a></p>
    </footer>

    <!-- Script -->
    <script>
// --- Theme Toggle (Dark / Light Mode) ---
const themeToggleBtn = document.getElementById('theme-toggle');
const body = document.body;

const savedTheme = localStorage.getItem('theme') || 'dark-mode';
body.className = savedTheme;
updateThemeIcon(savedTheme);

themeToggleBtn.addEventListener('click', () => {
    if (body.classList.contains('dark-mode')) {
        body.classList.replace('dark-mode', 'light-mode');
        localStorage.setItem('theme', 'light-mode');
        updateThemeIcon('light-mode');
    } else {
        body.classList.replace('light-mode', 'dark-mode');
        localStorage.setItem('theme', 'dark-mode');
        updateThemeIcon('dark-mode');
    }
});

function updateThemeIcon(theme) {
    const icon = themeToggleBtn.querySelector('i');
    icon.className = theme === 'dark-mode' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
}


// --- Model Image Mapping ---
const modelSelect = document.getElementById('input-model');
const carImg = document.getElementById('car-image');
const modelNameLabel = document.getElementById('car-model-name');
const classBadge = document.getElementById('car-class-badge');

const carImages = {
    'A-Class': {
        url: '__A_CLASS_URL__',
        name: 'A-Class',
        badge: 'Compact Hatchback'
    },
    'B-Class': {
        url: 'data:image/jpeg;base64,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',
        name: 'B-Class',
        badge: 'Premium MPV'
    },
    'C-Class': {
        url: '__C_CLASS_URL__',
        name: 'C-Class',
        badge: 'Executive Sedan'
    },
    'E-Class': {
        url: '__E_CLASS_URL__',
        name: 'E-Class',
        badge: 'Luxury Saloon'
    },
    'S-Class': {
        url: '__S_CLASS_URL__',
        name: 'S-Class',
        badge: 'Flagship Luxury'
    },
    'GLA': {
        url: '__GLA_URL__',
        name: 'GLA Class',
        badge: 'Compact SUV'
    },
    'GLC': {
        url: '__GLC_URL__',
        name: 'GLC Class',
        badge: 'Premium SUV'
    },
    'GLE': {
        url: '__GLE_URL__',
        name: 'GLE Class',
        badge: 'Luxury SUV'
    },
    'SLK': {
        url: '__SLK_URL__',
        name: 'SLK Roadster',
        badge: 'Sports Convertible'
    },
    'AMG GT': {
        url: 'data:image/jpeg;base64,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',
        name: 'AMG GT',
        badge: 'Super Sports Coupe'
    }
};

function updateCarVisual() {
    const selected = modelSelect.value;
    const info = carImages[selected];
    if (info) {
        carImg.src = info.url;
        modelNameLabel.textContent = info.name;
        classBadge.textContent = info.badge;
    }
}

modelSelect.addEventListener('change', updateCarVisual);
updateCarVisual(); // Initial load


// --- Sliders Value Updates ---
const sliders = [
    { id: 'input-year', valId: 'val-year', isLocale: false },
    { id: 'input-mileage', valId: 'val-mileage', isLocale: true },
    { id: 'input-engine', valId: 'val-engine', isLocale: false },
    { id: 'input-mpg', valId: 'val-mpg', isLocale: false },
    { id: 'input-tax', valId: 'val-tax', isLocale: false }
];

sliders.forEach(s => {
    const sliderEl = document.getElementById(s.id);
    const valueEl = document.getElementById(s.valId);
    
    sliderEl.addEventListener('input', () => {
        let val = sliderEl.value;
        if (s.isLocale) {
            valueEl.textContent = parseInt(val).toLocaleString('id-ID');
        } else {
            valueEl.textContent = val;
        }
    });
});


// --- Fuzzy Logic Core (Mamdani & Sugeno from scratch) ---

function triangle_member(x, a, b, c) {
    if (x <= a || x >= c) return 0;
    if (x === b) return 1;
    if (x > a && x < b) return (x - a) / (b - a);
    if (x > b && x < c) return (c - x) / (c - b);
    return 0;
}

function fuzzify_mileage(mileage) {
    return {
        Low: triangle_member(mileage, -40000, 0, 40000),
        Medium: triangle_member(mileage, 30000, 50000, 70000),
        High: triangle_member(mileage, 60000, 200000, 400000)
    };
}

function fuzzify_year(year) {
    return {
        Old: triangle_member(year, 2000, 2010, 2018),
        Medium: triangle_member(year, 2015, 2018, 2021),
        New: triangle_member(year, 2018, 2023, 2030)
    };
}

function fuzzify_engine(engine_size) {
    return {
        Kecil: triangle_member(engine_size, -1.0, 1.0, 2.0),
        Sedang: triangle_member(engine_size, 1.5, 2.5, 3.5),
        Besar: triangle_member(engine_size, 3.0, 4.5, 8.0)
    };
}

function fuzzify_mpg(mpg) {
    return {
        Boros: triangle_member(mpg, -20, 20, 40),
        Standar: triangle_member(mpg, 30, 50, 70),
        Irit: triangle_member(mpg, 60, 70, 120)
    };
}

function fuzzify_tax(tax) {
    return {
        Murah: triangle_member(tax, -100, 100, 200),
        Standar: triangle_member(tax, 150, 300, 450),
        Mahal: triangle_member(tax, 400, 600, 1500)
    };
}

function rule_evaluation_all(year, mileage, engine_size, mpg, tax) {
    const year_fuzzy = fuzzify_year(year);
    const mileage_fuzzy = fuzzify_mileage(mileage);
    const engine_fuzzy = fuzzify_engine(engine_size);
    const mpg_fuzzy = fuzzify_mpg(mpg);
    const tax_fuzzy = fuzzify_tax(tax);

    const rule1 = Math.min(year_fuzzy.New, mileage_fuzzy.Low, engine_fuzzy.Besar);
    const rule2 = Math.min(year_fuzzy.Old, mileage_fuzzy.High);
    const rule3 = Math.min(mpg_fuzzy.Irit, tax_fuzzy.Murah);
    const rule4 = Math.min(year_fuzzy.New, mileage_fuzzy.Low, mpg_fuzzy.Irit);
    const rule5 = Math.min(engine_fuzzy.Besar, tax_fuzzy.Mahal);
    const rule6 = Math.min(year_fuzzy.Old, mileage_fuzzy.High, mpg_fuzzy.Boros);
    const rule7 = Math.min(engine_fuzzy.Kecil, mpg_fuzzy.Irit);
    const rule8 = Math.min(tax_fuzzy.Mahal, mileage_fuzzy.Low);
    const rule9 = Math.min(year_fuzzy.Medium, mileage_fuzzy.Medium);
    const rule10 = Math.min(engine_fuzzy.Kecil, mileage_fuzzy.High);
    const rule11 = Math.min(year_fuzzy.New, engine_fuzzy.Besar);
    const rule12 = Math.min(year_fuzzy.Old, tax_fuzzy.Murah);
    const rule13 = Math.min(mpg_fuzzy.Boros, tax_fuzzy.Mahal);
    const rule14 = Math.min(mileage_fuzzy.Low, mpg_fuzzy.Irit);
    const rule15 = Math.min(engine_fuzzy.Sedang, year_fuzzy.Medium);
    const rule16 = Math.min(year_fuzzy.Medium, mpg_fuzzy.Standar);
    const rule17 = Math.min(mileage_fuzzy.Medium, tax_fuzzy.Standar);
    const rule18 = Math.min(engine_fuzzy.Sedang, mileage_fuzzy.Medium);
    const rule19 = Math.min(year_fuzzy.New, engine_fuzzy.Sedang);
    const rule20 = Math.min(year_fuzzy.Old, engine_fuzzy.Kecil);

    const rules_list = [
        rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
        rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20
    ];

    const agg_dict = {
        Murah: Math.max(rule2, rule6, rule10, rule12, rule13, rule20),
        Standar: Math.max(rule3, rule7, rule9, rule15, rule16, rule17),
        Premium: Math.max(rule4, rule14, rule18, rule19),
        Mewah: Math.max(rule1, rule5, rule8, rule11)
    };

    return { agg_dict, rules_list };
}

function defuzzify_mamdani(output_fuzzy) {
    const w_murah = output_fuzzy.Murah;
    const w_standar = output_fuzzy.Standar;
    const w_premium = output_fuzzy.Premium;
    const w_mewah = output_fuzzy.Mewah;

    let numerator = 0;
    let denominator = 0;

    // Discretize y from 0 to 100,000 in steps of 500
    for (let y = 0; y <= 100000; y += 500) {
        let mu_murah = triangle_member(y, 0, 3500, 15000);
        let mu_standar = triangle_member(y, 15000, 23500, 30000);
        let mu_premium = triangle_member(y, 26000, 28500, 40000);
        let mu_mewah = triangle_member(y, 45000, 75000, 150000);

        let mu_y = Math.max(
            Math.min(w_murah, mu_murah),
            Math.min(w_standar, mu_standar),
            Math.min(w_premium, mu_premium),
            Math.min(w_mewah, mu_mewah)
        );

        numerator += y * mu_y;
        denominator += mu_y;
    }

    if (denominator === 0) return 0;
    return numerator / denominator;
}

function defuzzify_sugeno(rules) {
    const z = [
        75000, 3500, 23500, 28500, 75000, 3500, 23500, 75000, 23500, 3500,
        75000, 3500, 3500, 28500, 23500, 23500, 23500, 28500, 28500, 3500
    ];
    let numerator = 0;
    let denominator = 0;

    for (let i = 0; i < 20; i++) {
        numerator += rules[i] * z[i];
        denominator += rules[i];
    }

    if (denominator === 0) return 0;
    return numerator / denominator;
}

function kategori_mobil(harga) {
    if (harga < 20000) return { name: "Economy", badge: "badge-economy" };
    if (harga < 35000) return { name: "Standard", badge: "badge-standard" };
    if (harga < 50000) return { name: "Premium", badge: "badge-premium" };
    return { name: "Luxury", badge: "badge-luxury" };
}


// --- Main Action Handler ---
const btnPredict = document.getElementById('btn-predict');
const priceMamdani = document.getElementById('price-mamdani');
const badgeMamdani = document.getElementById('badge-mamdani');
const priceSugeno = document.getElementById('price-sugeno');
const badgeSugeno = document.getElementById('badge-sugeno');

function performPrediction() {
    const year = parseInt(document.getElementById('input-year').value);
    const mileage = parseInt(document.getElementById('input-mileage').value);
    const engine = parseFloat(document.getElementById('input-engine').value);
    const mpg = parseFloat(document.getElementById('input-mpg').value);
    const tax = parseInt(document.getElementById('input-tax').value);

    // Calculate both
    const { agg_dict, rules_list } = rule_evaluation_all(year, mileage, engine, mpg, tax);
    const resMamdani = defuzzify_mamdani(agg_dict);
    const resSugeno = defuzzify_sugeno(rules_list);

    // Update Mamdani UI
    if (resMamdani === 0) {
        priceMamdani.textContent = "No Rule Active";
        badgeMamdani.textContent = "-";
        badgeMamdani.className = "result-badge";
    } else {
        priceMamdani.textContent = `$${resMamdani.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const cat = kategori_mobil(resMamdani);
        badgeMamdani.textContent = cat.name;
        badgeMamdani.className = `result-badge ${cat.badge}`;
    }

    // Update Sugeno UI
    if (resSugeno === 0) {
        priceSugeno.textContent = "No Rule Active";
        badgeSugeno.textContent = "-";
        badgeSugeno.className = "result-badge";
    } else {
        priceSugeno.textContent = `$${resSugeno.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const cat = kategori_mobil(resSugeno);
        badgeSugeno.textContent = cat.name;
        badgeSugeno.className = `result-badge ${cat.badge}`;
    }
}

// Perform initial prediction on page load
window.addEventListener('DOMContentLoaded', performPrediction);

// Perform prediction when sliders are moved (real-time)
sliders.forEach(s => {
    document.getElementById(s.id).addEventListener('input', performPrediction);
});

// Perform prediction when vehicle model changes
modelSelect.addEventListener('change', performPrediction);

// Also keep the manual button handler as a backup
btnPredict.addEventListener('click', performPrediction);


</script>
</body>
</html>

"""

if __name__ == "__main__":
    main()
