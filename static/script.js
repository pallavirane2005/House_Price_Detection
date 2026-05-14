document.getElementById('predictForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('.predict-btn');
    btn.innerText = '⏳ Predicting...';
    btn.disabled = true;

    try {
        const formData = new FormData(e.target);
        const data = {};
        const numFields = ['LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 'GrLivArea', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd', 'GarageCars', 'TotalBsmtSF'];
        
        formData.forEach((value, key) => {
            data[key] = numFields.includes(key) ? Number(value) : value;
        });

        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('priceValue').innerText = result.formatted_price;
            document.getElementById('result').classList.remove('hidden');
        } else {
            alert('Error: ' + result.error);
        }
    } catch (err) {
        alert('Failed to get prediction.');
    } finally {
        btn.innerText = '🔮 Predict Price';
        btn.disabled = false;
    }
});