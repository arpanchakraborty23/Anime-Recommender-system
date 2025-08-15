from flask import Flask, request, jsonify, render_template
from src.pipeline.recommendation_pipeline import AnimeRecommender
from src.pipeline.train_pipeline import TrainPipeline
from src.utils.logger import logging

app = Flask(__name__)
reco = AnimeRecommender()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/train")
def train():
    try:
        TrainPipeline().run_pipeline()
        return jsonify({
            "train": "successfully"
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route("/recommend", methods=['POST'])
def recommend():
    try:
        query = request.json

        if not query or "question" not in query:
            return jsonify({"error": "No question provided"}), 400

        user_question = query["question"]
        logging.info(f"Query received: {user_question}")

        # Get response from RAG model
        system_answer = reco.invoke(user_question)

        logging.info(f"Response of query: {system_answer}")

        return jsonify({"result": system_answer})

    except Exception as e:
        logging.error(f"Error in retrieval: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
