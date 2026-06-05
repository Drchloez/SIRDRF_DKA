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
        url: 'assets/a_class.jpg',
        name: 'A-Class',
        badge: 'Compact Hatchback'
    },
    'B-Class': {
        url: 'assets/a_class.jpg',
        name: 'B-Class',
        badge: 'Premium MPV'
    },
    'C-Class': {
        url: 'assets/c_class.jpg',
        name: 'C-Class',
        badge: 'Executive Sedan'
    },
    'E-Class': {
        url: 'assets/e_class.jpg',
        name: 'E-Class',
        badge: 'Luxury Saloon'
    },
    'S-Class': {
        url: 'assets/s_class.jpg',
        name: 'S-Class',
        badge: 'Flagship Luxury'
    },
    'GLA': {
        url: 'assets/g_glass.jpg',
        name: 'GLA Class',
        badge: 'Compact SUV'
    },
    'GLC': {
        url: 'assets/g_glass.jpg',
        name: 'GLC Class',
        badge: 'Premium SUV'
    },
    'GLE': {
        url: 'assets/g_glass.jpg',
        name: 'GLE Class',
        badge: 'Luxury SUV'
    },
    'SLK': {
        url: 'assets/sl_class.jpg',
        name: 'SLK Roadster',
        badge: 'Sports Convertible'
    },
    'AMG GT': {
        url: 'assets/sl_class.jpg',
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
        Low: triangle_member(mileage, 0, 20000, 40000),
        Medium: triangle_member(mileage, 30000, 50000, 70000),
        High: triangle_member(mileage, 60000, 80000, 100000)
    };
}

function fuzzify_year(year) {
    return {
        Old: triangle_member(year, 2010, 2014, 2018),
        Medium: triangle_member(year, 2015, 2018, 2021),
        New: triangle_member(year, 2018, 2021, 2023)
    };
}

function fuzzify_engine(engine_size) {
    return {
        Kecil: triangle_member(engine_size, 0, 1.0, 2.0),
        Sedang: triangle_member(engine_size, 1.5, 2.5, 3.5),
        Besar: triangle_member(engine_size, 3.0, 4.5, 6.0)
    };
}

function fuzzify_mpg(mpg) {
    return {
        Boros: triangle_member(mpg, 0, 20, 40),
        Standar: triangle_member(mpg, 30, 50, 70),
        Irit: triangle_member(mpg, 60, 70, 80)
    };
}

function fuzzify_tax(tax) {
    return {
        Murah: triangle_member(tax, 0, 100, 200),
        Standar: triangle_member(tax, 150, 300, 450),
        Mahal: triangle_member(tax, 400, 500, 600)
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
        Standar: Math.max(rule3, rule7, rule9, rule15, rule16, rule17, rule18),
        Mewah: Math.max(rule1, rule4, rule5, rule8, rule11, rule14, rule19)
    };

    return { agg_dict, rules_list };
}

function defuzzify_mamdani(output_fuzzy) {
    const w_murah = output_fuzzy.Murah;
    const w_standar = output_fuzzy.Standar;
    const w_mewah = output_fuzzy.Mewah;

    let numerator = 0;
    let denominator = 0;

    // Discretize y from 0 to 100,000 in steps of 500
    for (let y = 0; y <= 100000; y += 500) {
        let mu_murah = triangle_member(y, 0, 15000, 30000);
        let mu_standar = triangle_member(y, 20000, 35000, 50000);
        let mu_mewah = triangle_member(y, 40000, 50000, 100000);

        let mu_y = Math.max(
            Math.min(w_murah, mu_murah),
            Math.min(w_standar, mu_standar),
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
        50000, 15000, 35000, 50000, 50000, 15000, 35000, 50000, 35000, 15000,
        50000, 15000, 15000, 50000, 35000, 35000, 35000, 35000, 50000, 15000
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

btnPredict.addEventListener('click', () => {
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
});
