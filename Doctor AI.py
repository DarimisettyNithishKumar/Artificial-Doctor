from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyANEvIbgCdjoFiApq9PdA8UXfKnvy4wupc'
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Health Assistant</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        .container { max-width: 800px;}
        .content-section { display: none; }
        .content-section.active { display: block; }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="container bg-white rounded-xl shadow-lg p-8 space-y-8">
        <!-- Navigation Bar -->
        <nav class="flex justify-center space-x-4 mb-8">
            <button data-target="home-page" class="nav-button text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors duration-200">Home</button>
            <button data-target="health-tips" class="nav-button text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors duration-200">Health Tips</button>
        </nav>
        <!-- Home Page Section -->
        <div id="home-page" class="content-section active text-center space-y-8">
            <h1 class="text-3xl font-bold text-gray-800">Welcome to Your Personal Health Assistant</h1>
            <p class="text-gray-500">Choose an option below to get started:</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <button data-target="symptom-analyzer-page" class="nav-button bg-blue-500 text-white font-semibold py-4 px-6 rounded-lg shadow-md hover:bg-blue-600 transition-colors duration-200">
                    Symptom Analyzer
                </button>
                <button data-target="scanning-report-analyzer-page" class="nav-button bg-green-500 text-white font-semibold py-4 px-6 rounded-lg shadow-md hover:bg-green-600 transition-colors duration-200">
                    Scanning Report Analyzer
                </button>
                <button data-target="blood-report-analyzer-page" class="nav-button bg-red-500 text-white font-semibold py-4 px-6 rounded-lg shadow-md hover:bg-red-600 transition-colors duration-200">
                    Blood Report Analyzer
                </button>
                <button data-target="urine-test-analyzer-page" class="nav-button bg-yellow-500 text-white font-semibold py-4 px-6 rounded-lg shadow-md hover:bg-yellow-600 transition-colors duration-200">
                    Urine Test Analyzer
                </button>
            </div>
            <strong class="text-red-500 block mt-8">Disclaimer: This is for informational purposes only. Always consult a healthcare professional.</strong>
        </div>
        <!-- Symptom Analyzer Section -->
        <div id="symptom-analyzer-page" class="content-section space-y-8">
            <button class="back-btn bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg shadow hover:bg-gray-300 transition-colors duration-200" data-target="home-page">
                &larr; Back
            </button>
            <div class="text-center space-y-2">
                <h1 class="text-3xl font-bold text-gray-800">Symptom Analyzer</h1>
                <p class="text-gray-500">Enter a description of your symptoms below. (Uses <b>Natural Language Processing</b>)</p>
            </div>
            <div class="space-y-4">
                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-700">Describe Your Symptoms</label>
                    <textarea id="symptom-text-input" class="w-full h-32 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" placeholder="e.g., 'Fever, cough, and body aches'"></textarea>
                </div>
                <button data-input-id="symptom-text-input" data-file-input-id="" class="analyze-btn w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200">
                    Analyze Symptoms
                </button>
            </div>
            <div class="results-container bg-gray-50 rounded-lg p-6 space-y-4"></div>
        </div>
        <!-- Scanning Report Analyzer Section -->
        <div id="scanning-report-analyzer-page" class="content-section space-y-8">
            <button class="back-btn bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg shadow hover:bg-gray-300 transition-colors duration-200" data-target="home-page">
                &larr; Back
            </button>
            <div class="text-center space-y-2">
                <h1 class="text-3xl font-bold text-gray-800">Scanning Report Analyzer</h1>
                <p class="text-gray-500">Upload a scanning report image (e.g., X-ray, MRI, CT scan). (Uses <b>Computer Vision</b>)</p>
            </div>
            <div class="space-y-4">
                <div class="space-y-2">
                    <label for="scanning-report-input" class="block text-sm font-medium text-gray-700">Upload Report (Image)</label>
                    <input type="file" id="scanning-report-input" accept="image/*" class="w-full p-2 border border-gray-300 rounded-lg">
                </div>
                <button data-input-id="" data-file-input-id="scanning-report-input" class="analyze-btn w-full bg-green-600 text-white font-semibold py-3 rounded-lg hover:bg-green-700 transition-colors duration-200">
                    Analyze Report
                </button>
            </div>
            <div class="results-container bg-gray-50 rounded-lg p-6 space-y-4"></div>
        </div>
        <!-- Blood Report Analyzer Section -->
        <div id="blood-report-analyzer-page" class="content-section space-y-8">
            <button class="back-btn bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg shadow hover:bg-gray-300 transition-colors duration-200" data-target="home-page">
                &larr; Back
            </button>
            <div class="text-center space-y-2">
                <h1 class="text-3xl font-bold text-gray-800">Blood Report Analyzer</h1>
                <p class="text-gray-500">Upload a blood test report image. (Uses <b>Computer Vision</b>)</p>
            </div>
            <div class="space-y-4">
                <div class="space-y-2">
                    <label for="blood-report-input" class="block text-sm font-medium text-gray-700">Upload Report (Image)</label>
                    <input type="file" id="blood-report-input" accept="image/*" class="w-full p-2 border border-gray-300 rounded-lg">
                </div>
                <button data-input-id="" data-file-input-id="blood-report-input" class="analyze-btn w-full bg-red-600 text-white font-semibold py-3 rounded-lg hover:bg-red-700 transition-colors duration-200">
                    Analyze Report
                </button>
            </div>
            <div class="results-container bg-gray-50 rounded-lg p-6 space-y-4"></div>
        </div>
        <!-- Urine Test Analyzer Section -->
        <div id="urine-test-analyzer-page" class="content-section space-y-8">
            <button class="back-btn bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg shadow hover:bg-gray-300 transition-colors duration-200" data-target="home-page">
                &larr; Back
            </button>
            <div class="text-center space-y-2">
                <h1 class="text-3xl font-bold text-gray-800">Urine Test Analyzer</h1>
                <p class="text-gray-500">Upload a urine test report image. (Uses <b>Computer Vision</b>)</p>
            </div>
            <div class="space-y-4">
                <div class="space-y-2">
                    <label for="urine-test-input" class="block text-sm font-medium text-gray-700">Upload Report (Image)</label>
                    <input type="file" id="urine-test-input" accept="image/*" class="w-full p-2 border border-gray-300 rounded-lg">
                </div>
                <button data-input-id="" data-file-input-id="urine-test-input" class="analyze-btn w-full bg-yellow-600 text-white font-semibold py-3 rounded-lg hover:bg-yellow-700 transition-colors duration-200">
                    Analyze Report
                </button>
            </div>
            <div class="results-container bg-gray-50 rounded-lg p-6 space-y-4"></div>
        </div>
        <!-- Health Tips Section -->
        <div id="health-tips" class="content-section space-y-4">
            <div class="text-center space-y-2">
                <h1 class="text-3xl font-bold text-gray-800">Daily Health Tips</h1>
                <p class="text-gray-500">Select a body part to get specific health tips.</p>
            </div>
            <div id="body-parts-container" class="grid grid-cols-2 md:grid-cols-3 gap-4">
                <button data-body-part="Heart" class="tip-btn bg-white text-blue-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-blue-100 transition-colors duration-200">Heart</button>
                <button data-body-part="Brain" class="tip-btn bg-white text-green-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-green-100 transition-colors duration-200">Brain</button>
                <button data-body-part="Lungs" class="tip-btn bg-white text-red-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-red-100 transition-colors duration-200">Lungs</button>
                <button data-body-part="Stomach" class="tip-btn bg-white text-yellow-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-yellow-100 transition-colors duration-200">Stomach</button>
                <button data-body-part="Kidneys" class="tip-btn bg-white text-purple-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-purple-100 transition-colors duration-200">Kidneys</button>
                <button data-body-part="Skin" class="tip-btn bg-white text-pink-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-pink-100 transition-colors duration-200">Skin</button>
                <button data-body-part="Muscles" class="tip-btn bg-white text-indigo-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-indigo-100 transition-colors duration-200">Muscles</button>
                <button data-body-part="Eyes" class="tip-btn bg-white text-cyan-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-cyan-100 transition-colors duration-200">Eyes</button>
                <button data-body-part="Bones" class="tip-btn bg-white text-gray-500 font-semibold py-3 px-4 rounded-lg shadow hover:bg-gray-100 transition-colors duration-200">Bones</button>
            </div>
            <div id="tips-display" class="hidden">
                <button class="back-btn bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg shadow hover:bg-gray-300 transition-colors duration-200" data-target="health-tips">
                    &larr; Back
                </button>
                <div id="tip-card" class="bg-white rounded-lg shadow-md p-6 border-l-4 border-l-green-500 space-y-4">
                    <p id="tip-text" class="text-gray-700 italic">Tips will appear here.</p>
                </div>
            </div>
        </div>
    </div>
    <script>
        async function getPrognosis(prompt, imageData, resultsContainer) {
            resultsContainer.innerHTML = `
                <div id="loadingIndicator" class="text-center text-blue-500">
                    <p>Analyzing...</p>
                </div>`;
            try {
                const resp = await fetch("/analyze", {
                    method: "POST",
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ text: prompt, image: imageData })
                });
                const parsedData = await resp.json();
                const diseaseDescription = parsedData.disease_description || 'No description found.';
                const medicines = parsedData.medicines || [];
                const resultsWrapper = document.createElement('div'); resultsWrapper.id = "analysisResults";
                resultsWrapper.className = "space-y-4";
                resultsContainer.innerHTML = ''; resultsContainer.appendChild(resultsWrapper);
                const titleEl = document.createElement('h2'); titleEl.className = 'text-xl font-semibold text-gray-700';
                titleEl.textContent = 'Analysis Results'; resultsWrapper.appendChild(titleEl);
                const diseaseInfoEl = document.createElement('div'); diseaseInfoEl.id = 'diseaseInfo';
                diseaseInfoEl.className = 'mt-4';
                diseaseInfoEl.innerHTML = `<h3 class="font-semibold text-gray-700">Disease Description</h3>
                    <div class="mt-2 text-gray-600 leading-relaxed">${diseaseDescription}</div>`;
                resultsWrapper.appendChild(diseaseInfoEl);
                const medicineInfoEl = document.createElement('div'); medicineInfoEl.id = 'medicineInfo';
                medicineInfoEl.className = 'mt-4';
                medicineInfoEl.innerHTML = `<h3 class="font-semibold text-gray-700">Recommended Medicines</h3>
                        <div id="medicineList" class="mt-2 text-gray-600 leading-relaxed"></div>`;
                resultsWrapper.appendChild(medicineInfoEl);
                const medicineListDiv = document.getElementById('medicineList');
                if (medicines.length > 0) {
                    medicines.forEach(medicine => {
                        const medicineItem = document.createElement('div');
                        medicineItem.className = 'mb-4';
                        const nameEl = document.createElement('p'); nameEl.className = 'font-semibold text-gray-800'; nameEl.textContent = medicine.name;
                        const formEl = document.createElement('p'); formEl.className = 'text-sm text-gray-500 italic'; formEl.textContent = `Form: ${medicine.form}`;
                        const brandsEl = document.createElement('p'); brandsEl.className = 'text-gray-600 mt-1'; brandsEl.textContent = `Common Brands: ${medicine.brands.join(', ')}`;
                        medicineItem.appendChild(nameEl); medicineItem.appendChild(formEl); medicineItem.appendChild(brandsEl);
                        medicineListDiv.appendChild(medicineItem);
                    });
                } else {
                    medicineListDiv.textContent = 'No specific medicines found.';
                }
            } catch (error) {
                resultsContainer.innerHTML = `<div class="text-red-500 text-center"><p>An error occurred. Please try again.</p></div>`;
            }
        }

        async function getTipsForBodyPart(bodyPart) {
            const tipTextDiv = document.getElementById('tip-text');
            tipTextDiv.innerHTML = `<div id="loadingIndicator" class="text-center text-blue-500"><p>Fetching tips...</p></div>`;
            const resp = await fetch("/tips", {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ bodyPart })
            });
            const tips = await resp.json();
            if (Array.isArray(tips) && tips.length > 0) {
                const tipListHtml = tips.map(tip => `<li>${tip}</li>`).join('');
                tipTextDiv.innerHTML = `<ul class="list-disc list-inside space-y-2">${tipListHtml}</ul>`;
            } else {
                tipTextDiv.innerHTML = `<p>No tips found for this body part. Please try another.</p>`;
            }
        }

        function navigateTo(targetId) {
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(targetId).classList.add('active');
        }
        document.querySelectorAll('.nav-button').forEach(button => {
            button.addEventListener('click', (e) => {
                navigateTo(e.target.dataset.target);
            });
        });
        document.querySelectorAll('.analyze-btn').forEach(button => {
            button.addEventListener('click', async () => {
                const textInputId = button.dataset.inputId;
                const fileInputId = button.dataset.fileInputId;
                const parentSection = button.closest('.content-section');
                const resultsContainer = parentSection.querySelector('.results-container');
                const textInput = textInputId ? document.getElementById(textInputId).value.trim() : null;
                const fileInput = fileInputId ? document.getElementById(fileInputId) : null;
                const file = fileInput?.files?.[0];
                if (!textInput && !file) {
                    resultsContainer.innerHTML = `<div class="text-red-500 text-center"><p>Please enter symptoms or upload a report to get a diagnosis.</p></div>`;
                    return;
                }
                if (file) {
                    const reader = new FileReader();
                    reader.onload = async function(e) {
                        await getPrognosis(textInput, e.target.result, resultsContainer);
                    };
                    reader.readAsDataURL(file);
                } else if (textInput) {
                    await getPrognosis(textInput, null, resultsContainer);
                }
            });
        });
        document.querySelectorAll('.tip-btn').forEach(button => {
            button.addEventListener('click', () => {
                const bodyPart = button.dataset.bodyPart;
                document.getElementById('body-parts-container').classList.add('hidden');
                document.getElementById('tips-display').classList.remove('hidden');
                getTipsForBodyPart(bodyPart);
            });
        });
        document.querySelectorAll('.back-btn').forEach(button => {
            button.addEventListener('click', () => {
                const targetId = button.dataset.target;
                if (targetId === 'home-page') {
                    navigateTo('home-page');
                } else if (targetId === 'health-tips') {
                    document.getElementById('tips-display').classList.add('hidden');
                    document.getElementById('body-parts-container').classList.remove('hidden');
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text")
    image = data.get("image")
    prompt = (
        "Analyze the provided information. Identify the disease and any explicit prescriptions. "
        "For each medicine, specify its form and a list of well-known brand names. "
        "If no medicines are explicitly mentioned, based on the identified disease, provide a list of common, over-the-counter medicines. "
        "Adhere strictly to the provided JSON schema. Always return the JSON object even if no information is found; "
        "in that case, the fields can be empty or null.\n\n"
        '{ "disease_description": "text", "medicines": [{ "name": "medicine name", "form": "form (e.g., tablet, syrup)", "brands": ["brand 1", "brand 2"] }] }'
    )
    parts = []
    if text:
        parts.append({"text": f"Context: {text}."})
    parts.append({"text": prompt})
    if image:
        parts.append({
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": image.split(",")[1]
            }
        })
    payload = {
        "contents": [{
            "role": "user",
            "parts": parts
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "disease_description": { "type": "STRING" },
                    "medicines": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "name": { "type": "STRING" },
                                "form": { "type": "STRING" },
                                "brands": {
                                    "type": "ARRAY",
                                    "items": { "type": "STRING" }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    resp = requests.post(API_URL, json=payload)
    if not resp.ok:
        return jsonify({'error': 'Gemini API error', 'status': resp.status_code})
    result = resp.json()
    try:
        text_json = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify(eval(text_json))
    except Exception:
        return jsonify({'error': 'Parsing Gemini response failed', 'raw': result})

@app.route("/tips", methods=["POST"])
def tips():
    data = request.json
    body_part = data.get("bodyPart")
    prompt = (
        f"Generate a list of at least 20 concise and helpful health tips for the {body_part} part of the human body. "
        "The tips should be formatted as a JSON array of strings. Do not include any introductory phrases or headings."
    )
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{ "text": prompt }]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            }
        }
    }
    resp = requests.post(API_URL, json=payload)
    if not resp.ok:
        return jsonify([])
    result = resp.json()
    try:
        text_json = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify(eval(text_json))
    except Exception:
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)
