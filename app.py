import streamlit as st
import numpy as np

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
        mu_murah = triangle_member(y, 0, 12000, 22000)
        mu_standar = triangle_member(y, 18000, 28000, 38000)
        mu_premium = triangle_member(y, 32000, 42000, 52000)
        mu_mewah = triangle_member(y, 48000, 75000, 120000)

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
    # Output konstan (singleton) untuk masing-masing 20 aturan
    z = [
        75000, 12000, 28000, 42000, 75000, 12000, 28000, 75000, 28000, 12000,
        75000, 12000, 12000, 42000, 28000, 28000, 28000, 42000, 42000, 12000
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


def load_custom_style():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            font-family: 'Poppins', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Prediksi Harga Mobil Bekas", page_icon="🚗")
    load_custom_style()

    st.title("🚗 Prediksi Harga Mobil Bekas")
    st.write(
        "✨ Aplikasi logika fuzzy Mamdani & Sugeno untuk mengestimasi harga mobil bekas "
        "berdasarkan spesifikasi kendaraan."
    )

    st.sidebar.title("📌 Tentang Project")
    st.sidebar.write(
        "🧠 Project Dasar Kecerdasan AI menggunakan metode Fuzzy Mamdani & Sugeno "
        "untuk estimasi harga mobil bekas Mercedes-Benz."
    )
    st.sidebar.markdown(
        "📂 **Dataset Source:**\n"
        "[Kaggle Mercedes Used Car Dataset](https://www.kaggle.com/datasets/koki2525/mercedes-benz-used-car-dataset)"
    )

    st.subheader("📝 Input Data Mobil")
    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input("📅 Tahun Mobil", min_value=2010, max_value=2025, value=2020)
        mileage = st.number_input("🛣️ Mileage", min_value=0, max_value=200000, value=30000)
        engine_size = st.number_input(
            "⚙️ Engine Size",
            min_value=0.0,
            max_value=6.5,
            value=1.5,
            step=0.1,
        )

    with col2:
        mpg = st.number_input(
            "⛽ MPG",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=0.1,
        )
        tax = st.number_input("💸 Tax", min_value=0, max_value=1000, value=150)

    st.divider()

    if st.button("🔍 Prediksi", type="primary"):
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown("### 🔴 Fuzzy Mamdani")
            harga_mamdani = prediksi_harga(year, mileage, engine_size, mpg, tax, method="Mamdani")
            kat_mamdani = kategori_mobil(harga_mamdani)
            if harga_mamdani == 0:
                st.warning("⚠️ Tidak ada rule fuzzy yang aktif.")
            else:
                st.metric(label="Estimasi Harga (Centroid)", value=f"${harga_mamdani:,.2f}")
                st.info(f"🏆 Kategori: {kat_mamdani}")
                
        with col_res2:
            st.markdown("### 🟢 Fuzzy Sugeno")
            harga_sugeno = prediksi_harga(year, mileage, engine_size, mpg, tax, method="Sugeno")
            kat_sugeno = kategori_mobil(harga_sugeno)
            if harga_sugeno == 0:
                st.warning("⚠️ Tidak ada rule fuzzy yang aktif.")
            else:
                st.metric(label="Estimasi Harga (Weighted Avg)", value=f"${harga_sugeno:,.2f}")
                st.info(f"🏆 Kategori: {kat_sugeno}")


if __name__ == "__main__":
    main()
