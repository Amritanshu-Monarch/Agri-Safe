from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# RAG imports
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

app = Flask(__name__)
CORS(app)

# ================= CNN MODEL =================
model = load_model("model.h5")

class_names = ["Healthy", "Leaf Spot", "Blight", "Rust"]  # change based on your dataset

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']

    img = Image.open(file).resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    result = class_names[np.argmax(pred)]

    return jsonify({
        "disease": result,
        "confidence": float(np.max(pred))
    })

# ================= RAG CHATBOT =================

loader = TextLoader("rag_data.txt")
docs = loader.load()

embeddings = OpenAIEmbeddings()  # add OPENAI_API_KEY in env
db = FAISS.from_documents(docs, embeddings)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=db.as_retriever()
)

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    answer = qa.run(query)

    return jsonify({"answer": answer})

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
