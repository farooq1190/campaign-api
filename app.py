from flask import Flask, jsonify, request
from extensions import db, bcrypt
from utils.validators import validate_campaign_data
from models.campaign import Campaign
from services.analytics import campaign_report
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from routes.auth import auth_bp
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


app = Flask(__name__)
# Database connection string
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)


@app.route("/")
def home():
    return jsonify({"message": "Campaign API is running!"})


@app.route("/campaigns", methods=["POST"])
@jwt_required()
def create_campaign():
    data = request.get_json()
    result = validate_campaign_data(data)
    if not result["valid"]:
        return jsonify({"errors": result["errors"]}), 400
    
    existing_campaign = Campaign.query.get(data["id"])
    if existing_campaign:     
        return jsonify({"error": f"Campaign with ID '{data['id']}' already exists."}), 400
    campaign = Campaign(
        id=data["id"],
        budget=data["budget"],
        impressions=data["impressions"],
        clicks=data["clicks"],
        spend=data["spend"],
        leads=data["leads"],
        conversions=data["conversions"],
        revenue=data["revenue"]
    )

    db.session.add(campaign)
    db.session.commit()
    return jsonify({"message": f"Campaign '{campaign.id}' created successfully"}), 201

#READ ALL — GET /campaigns
@app.route("/campaigns", methods=["GET"])
@jwt_required()

def get_all_campaigns():
    campaigns = Campaign.query.all()
    if not campaigns:
        return jsonify({"message": "No campaigns found."}), 200
    reports = jsonify([campaign_report(c) for c in campaigns])
    return reports, 200

#READ ONE — GET /campaigns/<id>
@app.route("/campaigns/<string:campaign_id>", methods=["GET"])
@jwt_required()
def get_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404
    return jsonify(campaign_report(campaign)), 200


# UPDATE — PUT /campaigns/<id>
@app.route("/campaigns/<string:campaign_id>", methods=["PUT"])
@jwt_required()
def update_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404

    data = request.get_json()
    result = validate_campaign_data(data)
    if not result["valid"]:
        return jsonify({"errors": result["errors"]}), 400
    
    campaign.budget      = data["budget"]
    campaign.impressions = data["impressions"]
    campaign.clicks      = data["clicks"]
    campaign.spend       = data["spend"]
    campaign.leads       = data["leads"]
    campaign.conversions = data["conversions"]
    campaign.revenue     = data["revenue"]
       
    
    db.session.add(campaign)
    db.session.commit()
    return jsonify({"message": f"Campaign '{campaign_id}' updated successfully"}), 200


#DELETE — DELETE /campaigns/<id>

@app.route("/campaigns/<string:campaign_id>", methods=["DELETE"])
@jwt_required()
def delete_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404
    
    db.session.delete(campaign)
    db.session.commit()

    return jsonify({"message": f"Campaign '{campaign_id}' deleted successfully"}), 200



# PARTIAL UPDATE — PATCH /campaigns/<id>
@app.route("/campaigns/<string:campaign_id>", methods=["PATCH"])
@jwt_required()
def patch_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404

    data = request.get_json()
    campaign = Campaign.query.get(campaign_id)

    # only update fields that were sent
    if "budget" in data:
        campaign.budget = data["budget"]
    if "impressions" in data:
        campaign.impressions = data["impressions"]
    if "clicks" in data:
        campaign.clicks = data["clicks"]
    if "spend" in data:
        campaign.spend = data["spend"]
    if "leads" in data:
        campaign.leads = data["leads"]
    if "conversions" in data:
        campaign.conversions = data["conversions"]
    if "revenue" in data:
        campaign.revenue = data["revenue"]

    db.session.add(campaign)
    db.session.commit() 
    return jsonify({"message": f"Campaign '{campaign_id}' updated successfully"}), 200


if __name__ == "__main__":
    app.run(debug=False)