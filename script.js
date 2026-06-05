// --- Theme Toggle (Dark / Light Mode) ---
const themeToggleBtn = document.getElementById('theme-toggle');
const body = document.body;

// Check stored theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.className = savedTheme;
    updateThemeIcon(savedTheme);
} else {
    // Default to dark mode
    body.className = 'dark-mode';
    updateThemeIcon('dark-mode');
}

themeToggleBtn.addEventListener('click', () => {
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        localStorage.setItem('theme', 'light-mode');
        updateThemeIcon('light-mode');
    } else {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark-mode');
        updateThemeIcon('dark-mode');
    }
});

function updateThemeIcon(theme) {
    const icon = themeToggleBtn.querySelector('i');
    if (theme === 'dark-mode') {
        icon.className = 'fa-solid fa-moon';
    } else {
        icon.className = 'fa-solid fa-sun';
    }
}


// --- Mini Interactive Fuzzy Simulator ---
const sliderYear = document.getElementById('input-year');
const sliderMileage = document.getElementById('input-mileage');
const valYear = document.getElementById('val-year');
const valMileage = document.getElementById('val-mileage');
const fuzzyResult = document.getElementById('fuzzy-result');

function triangleMember(x, a, b, c) {
    if (x <= a || x >= c) return 0;
    if (x === b) return 1;
    if (x > a && x < b) return (x - a) / (b - a);
    if (x > b && x < c) return (c - x) / (c - b);
    return 0;
}

function calculateFuzzyCategory(year, mileage) {
    // Fuzzify Year (Old, Medium, New)
    let yOld = triangleMember(year, 2010, 2014, 2018);
    let yMedium = triangleMember(year, 2015, 2018, 2021);
    let yNew = triangleMember(year, 2018, 2021, 2023);

    // Fuzzify Mileage (Low, Medium, High)
    let mLow = triangleMember(mileage, 0, 20000, 40000);
    let mMedium = triangleMember(mileage, 30000, 50000, 70000);
    let mHigh = triangleMember(mileage, 60000, 80000, 100000);

    // Rules
    let rMewah = Math.min(yNew, mLow);
    let rMurah = Math.min(yOld, mHigh);
    let rStandar = Math.min(yMedium, mMedium);

    // Boost fallback rules if input is extreme but rules don't overlap perfectly
    if (year >= 2021 && mileage <= 25000) rMewah = Math.max(rMewah, 0.9);
    if (year <= 2013 && mileage >= 65000) rMurah = Math.max(rMurah, 0.9);

    let sumWeights = rMurah + rStandar + rMewah;
    let price = 30000; // default standard

    if (sumWeights > 0) {
        price = (rMurah * 15000 + rStandar * 35000 + rMewah * 55000) / sumWeights;
    } else {
        // Fallback interpolation based on inputs
        let ageFactor = (year - 2010) / 13; // 0 to 1
        let mileageFactor = Math.max(0, 1 - (mileage / 100000)); // 1 to 0
        price = 10000 + (ageFactor * 32000) + (mileageFactor * 22000);
    }

    // Determine class & CSS styles
    if (price < 20000) return { name: "Economy", badge: "badge-economy" };
    if (price < 35000) return { name: "Standard", badge: "badge-standard" };
    if (price < 50000) return { name: "Premium", badge: "badge-premium" };
    return { name: "Luxury", badge: "badge-luxury" };
}

function updateSimulator() {
    const year = parseInt(sliderYear.value);
    const mileage = parseInt(sliderMileage.value);

    // Update UI text
    valYear.textContent = year;
    valMileage.textContent = mileage.toLocaleString('id-ID');

    // Run fuzzy model
    const result = calculateFuzzyCategory(year, mileage);

    // Update Result UI
    fuzzyResult.textContent = result.name;
    fuzzyResult.className = `result-badge ${result.badge}`;
}

// Add event listeners for sliders
sliderYear.addEventListener('input', updateSimulator);
sliderMileage.addEventListener('input', updateSimulator);

// Initial calculation
updateSimulator();
