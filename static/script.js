const featureContainer = document.getElementById("features");

// Create V1 to V28 input fields
for (let i = 1; i <= 28; i++) {

    const input = document.createElement("input");

    input.type = "number";
    input.id = "V" + i;
    input.placeholder = "V" + i;
    input.value = "0";
    input.step = "any";
    input.required = true;

    featureContainer.appendChild(input);
}


// Handle transaction form
document.getElementById("fraudForm").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const result = document.getElementById("result");

        result.innerText = "Analyzing transaction...";

        const data = {};

        data.Time = Number(document.getElementById("Time").value);

        data.Amount = Number(document.getElementById("Amount").value);

        for (let i = 1; i <= 28; i++) {

            data["V" + i] = Number(
                document.getElementById("V" + i).value
            );

        }

        try {

            const response = await fetch("/predict", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)

            });

            const output = await response.json();

            if (!response.ok) {
                throw new Error(output.error || "Prediction failed");
            }

            result.innerHTML = `
                <h3>${output.result}</h3>
                <p>Fraud Probability:
                ${(output.fraud_probability * 100).toFixed(2)}%</p>
            `;
            await refreshDashboard();

        }

        catch(error) {

            result.innerText = "Error: " + error.message;

        }

    }
);
// Load dashboard statistics

async function loadStats() {

    const response = await fetch("/stats");
    const data = await response.json();

    document.getElementById("total").innerText = data.total;

    document.getElementById("fraud").innerText = data.fraud;

    document.getElementById("legitimate").innerText =
        data.legitimate;
}


// Load transaction history

async function loadHistory() {

    const response = await fetch("/history");

    const data = await response.json();

    const table = document.getElementById("historyTable");

    table.innerHTML = "";

    data.forEach(item => {

        const row = document.createElement("tr");

        const values = [
            item.id,
            item.amount,
            item.result,
            (item.fraud_probability * 100).toFixed(2) + "%"
        ];

        values.forEach(value => {

            const cell = document.createElement("td");

            cell.textContent = value;

            row.appendChild(cell);

        });

        table.appendChild(row);

    });

}


// Refresh dashboard

async function refreshDashboard() {

    await loadStats();

    await loadHistory();

}

refreshDashboard();