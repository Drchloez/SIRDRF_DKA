import streamlit as st


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
    low = triangle_member(mileage, 0, 20000, 40000)
    medium = triangle_member(mileage, 30000, 50000, 70000)
    high = triangle_member(mileage, 60000, 80000, 100000)

    return {"Low": low, "Medium": medium, "High": high}


def fuzzify_year(year):
    old = triangle_member(year, 2010, 2014, 2018)
    medium = triangle_member(year, 2015, 2018, 2021)
    new = triangle_member(year, 2018, 2021, 2023)

    return {"Old": old, "Medium": medium, "New": new}


def fuzzify_engine(engine_size):
    kecil = triangle_member(engine_size, 0, 1.0, 2.0)
    sedang = triangle_member(engine_size, 1.5, 2.5, 3.5)
    besar = triangle_member(engine_size, 3.0, 4.5, 6.0)

    return {"Kecil": kecil, "Sedang": sedang, "Besar": besar}


def fuzzify_mpg(mpg):
    boros = triangle_member(mpg, 0, 20, 40)
    standar = triangle_member(mpg, 30, 50, 70)
    irit = triangle_member(mpg, 60, 70, 80)

    return {"Boros": boros, "Standar": standar, "Irit": irit}


def fuzzify_tax(tax):
    murah = triangle_member(tax, 0, 100, 200)
    standar = triangle_member(tax, 150, 300, 450)
    mahal = triangle_member(tax, 400, 500, 600)

    return {"Murah": murah, "Standar": standar, "Mahal": mahal}


def rule_evaluation(year, mileage, engine_size, mpg, tax):
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

    return {
        "Murah": max(rule2, rule6, rule10, rule12, rule13, rule20),
        "Standar": max(rule3, rule7, rule9, rule15, rule16, rule17, rule18),
        "Mewah": max(rule1, rule4, rule5, rule8, rule11, rule14, rule19),
    }


def defuzzification(output_fuzzy):
    murah = output_fuzzy["Murah"]
    standar = output_fuzzy["Standar"]
    mewah = output_fuzzy["Mewah"]

    harga_murah = 15000
    harga_standar = 35000
    harga_mewah = 50000

    numerator = (murah * harga_murah + standar * harga_standar + mewah * harga_mewah)
    denominator = murah + standar + mewah

    if denominator == 0:
        return 0

    return numerator / denominator


def prediksi_harga(year, mileage, engine_size, mpg, tax):
    fuzzy_output = rule_evaluation(year, mileage, engine_size, mpg, tax)
    return defuzzification(fuzzy_output)


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
        "✨ Aplikasi fuzzy Mamdani untuk mengestimasi harga mobil bekas "
        "berdasarkan spesifikasi kendaraan."
    )

    st.sidebar.title("📌 Tentang Project")
    st.sidebar.write(
        "🧠 Project Dasar Kecerdasan AI menggunakan metode Fuzzy Mamdani "
        "untuk estimasi harga mobil bekas."
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
        harga = prediksi_harga(year, mileage, engine_size, mpg, tax)
        kategori = kategori_mobil(harga)

        if harga == 0:
            st.warning("⚠️ Tidak ada rule fuzzy yang aktif untuk input tersebut.")
        else:
            st.success(f"💰 Prediksi Harga: ${harga:,.2f}")
            st.info(f"🏆 Kategori Mobil: {kategori}")

if __name__ == "__main__":
    main()
