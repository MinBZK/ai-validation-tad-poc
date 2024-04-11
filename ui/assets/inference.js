import * as ort from "https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/esm/ort.min.js";

ort.env.wasm.wasmPaths = "https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/";

let probabilityDistribution;

async function main() {
    try {
        const runButton = document.getElementById('runInference');
        runButton.addEventListener('click', async () => {
            const outputProbabilitiesField = "probabilities";
            const outputClassField = "label";
            const inputName = "float_input";

            const modelName = document.getElementById('modelurl').getAttribute("href");
            const session = await ort.InferenceSession.create(modelName);
            const outputContainer = document.getElementById('outputContainer');
            const outputLabel = document.getElementById('label');

            const inputValues = [];
            var inputs = document.querySelectorAll('input[id^="input."]');
            inputs.forEach(function (input) {
                inputValues.push(parseFloat(input.value));
            });

            const inputTensorShape = [1, inputValues.length]; // Adjusting tensor shape
            const tensor = new ort.Tensor('float32', inputValues, inputTensorShape); // Adjusting tensor shape
            const feeds = {
                [inputName]: tensor
            };
            const results = await session.run(feeds);
            const data = results[outputProbabilitiesField].data;
            document.getElementById("inferenceResultsContainer").style.display = "block";
            outputContainer.innerHTML = '';
            let graphData = [];
            let graphLabels = [];
            data.forEach((probability, index) => {
                graphLabels.push("Class " + index);
                graphData.push(probability.toFixed(2));
            });

            if (outputClassField) {
                outputLabel.textContent = "Class " + results[outputClassField].data;
            }
            renderGraph(graphData, graphLabels);
        });
    } catch (e) {
        const errorElement = document.getElementById('error');
        errorElement.textContent = `Failed to inference model: ${e}`;
        console.error('Failed to inference model:', e);
    }
}

main();

function renderGraph(data, labels) {
    const ctx = document.getElementById('probabilityChart');

    if (probabilityDistribution) {
        probabilityDistribution.destroy();
    }

    probabilityDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,

            datasets: [{
                backgroundColor: ["rgba(0, 123, 199, 0.8)"],
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            plugins:
                {
                    legend: {
                        display: false
                    }
                },
            scales: {
                y: {
                    title: {
                        text: 'Probability',
                        display: true
                    },
                    beginAtZero: true,
                    max: 1,
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}
