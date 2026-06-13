from flask import Flask, jsonify, request
from extensions import db, bcrypt
from utils.validators import validate_campaign_data
from models.campaign import Campaign
from services.analytics import campaign_report
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from routes.auth import auth_bp
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


app = Flask(__name__)
CORS(app)
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
    return """
    <html>
    <head><title>Campaign Analytics API</title></head>
    <body>
        <h1>Campaign Analytics API</h1>
        <p>Built with Python, Flask, PostgreSQL, JWT Authentication</p>
        <p>A REST API for managing digital marketing campaigns with real KPIs — CTR, CPL, ROAS</p>
        <p><a href="https://github.com/farooq1190/campaign-api">View on GitHub</a></p>
    </body>
    </html>
    """   


@app.route("/campaigns", methods=["POST"])
@jwt_required()
def create_campaign():
    data = request.get_json()
    result = validate_campaign_data(data)
    if not result["valid"]:
        return jsonify({"errors": result["errors"]}), 400
    
    user_id = int(get_jwt_identity())
    
    campaign = Campaign(
        name=data["name"],
        budget=data["budget"],
        impressions=data["impressions"],
        clicks=data["clicks"],
        spend=data["spend"],
        leads=data["leads"],
        conversions=data["conversions"],
        revenue=data["revenue"],
        user_id=user_id
    )

    db.session.add(campaign)
    db.session.commit()
    return jsonify({"message": f"Campaign '{data['name']}' created successfully"}), 201

#READ ALL — GET /campaigns
@app.route("/campaigns", methods=["GET"])
@jwt_required()

def get_all_campaigns():
    user_id = int(get_jwt_identity())
    campaigns = Campaign.query.filter_by(user_id=user_id).all()
    if not campaigns:
        return jsonify({"message": "No campaigns found"}), 404

    reports = jsonify([campaign_report(c) for c in campaigns])
    return reports, 200

#READ ONE — GET /campaigns/<id>
@app.route("/campaigns/<string:campaign_id>", methods=["GET"])
@jwt_required()
def get_campaign(campaign_id):
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first()
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404
    return jsonify(campaign_report(campaign)), 200


# UPDATE — PUT /campaigns/<id>
@app.route("/campaigns/<string:campaign_id>", methods=["PUT"])
@jwt_required()
def update_campaign(campaign_id):
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first()
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404

    data = request.get_json()
    result = validate_campaign_data(data)
    if not result["valid"]:
        return jsonify({"errors": result["errors"]}), 400
    
    
    campaign.name        = data["name"]
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
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first()
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404
    
    db.session.delete(campaign)
    db.session.commit()

    return jsonify({"message": f"Campaign '{campaign_id}' deleted successfully"}), 200



# PARTIAL UPDATE — PATCH /campaigns/<id>
@app.route("/campaigns/<string:campaign_id>", methods=["PATCH"])
@jwt_required()
def patch_campaign(campaign_id):
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first()
    if not campaign:
        return jsonify({"error": f"Campaign '{campaign_id}' not found"}), 404

    data = request.get_json()
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first()

    # only update fields that were sent
    if "name" in data:
        campaign.name = data["name"]
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