# models/campaign.py
from extensions import db

class Campaign(db.Model):
    __tablename__ = "campaigns"


    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(100), nullable=False)
    budget      = db.Column(db.Integer, nullable=False)
    impressions = db.Column(db.Integer, nullable=False)
    clicks      = db.Column(db.Integer, nullable=False)
    spend       = db.Column(db.Integer, nullable=False)
    leads       = db.Column(db.Integer, nullable=False)
    conversions = db.Column(db.Integer, nullable=False)
    revenue     = db.Column(db.Integer, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name, budget, impressions, clicks, spend, leads, conversions, revenue, user_id):
    
        self.name        = name
        self.budget      = budget
        self.impressions = impressions
        self.clicks      = clicks
        self.spend       = spend
        self.leads       = leads
        self.conversions = conversions
        self.revenue     = revenue
        self.user_id     = user_id
    