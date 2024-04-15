import * as ort from "https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/esm/ort.min.js";
ort.env.wasm.wasmPaths = "https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/";
async function main() {
    try {
        const runButton = document.getElementById('runInference');
        runButton.addEventListener('click', async () => {
            const outputProbabilitiesField = "probabilities";
            const outputClassField = "label";
            const inputName = "float_input";

            const modelName = document.getElementById('modelurl').value
            const session = await ort.InferenceSession.create(modelName);
            const outputContainer = document.getElementById('outputContainer');
            const outputLabel = document.getElementById('label');

            const inputValues = [];
            var inputs = document.querySelectorAll('input[id^="input."]');
            inputs.forEach(function(input) {
                inputValues.push(parseFloat(input.value));
            });

            const inputTensorShape = [1, inputValues.length]; // Adjusting tensor shape
            const tensor = new ort.Tensor('float32', inputValues, inputTensorShape); // Adjusting tensor shape
            const feeds = {
                [inputName]: tensor
            };
            const results = await session.run(feeds);
            const data = results[outputProbabilitiesField].data;
            outputContainer.innerHTML = '';
            data.forEach((probability, index) => {
                const div = document.createElement('div');
                div.textContent = `Class ${index}: ${probability.toFixed(2)}`;
                outputContainer.appendChild(div);
            });

            if (outputClassField) {
                outputLabel.textContent = results[outputClassField].data;
            }
        });
   } catch (e) {
        const errorElement = document.getElementById('error');
        errorElement.textContent = `Failed to inference model: ${e}`;
        console.error('Failed to inference model:', e);
   }
}
main();
