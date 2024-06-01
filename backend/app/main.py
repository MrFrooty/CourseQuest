from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from linkedin_scraper import scrape_linkedin_profile
from summarizer import summarize_profile
from stable_diffusion import generate_image

app = Flask(__name__)
CORS(app)


class ProfileInput(BaseModel):
    linkedin_url: str
    username: str
    password: str

class ImageRequest(BaseModel):
    linkedin_url: str
    selected_info: dict


@app.route("/health", methods=["GET"])
def health():
    try:
        # Here you can add any logic to check the health of your application,
        # like checking database connectivity, etc.
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        profile_input = ProfileInput(**data)
        print(profile_input)

        scraped_data = scrape_linkedin_profile(profile_input.linkedin_url, profile_input.username, profile_input.password)
        return jsonify({"data": scraped_data})
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Parse and validate request data
        data = request.get_json()
        image_request = ImageRequest(**data)

        # Summarize profile and generate image
        summary = summarize_profile(image_request.selected_info)
        image = generate_image(summary)
        return jsonify({"image": image})
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
