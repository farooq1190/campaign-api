# models/campaign.py
from extensions import db

class Campaign(db.Model):
    __tablename__ = "campaigns"

    id          = db.Column(db.String(100), primary_key=True)
    budget      = db.Column(db.Integer, nullable=False)
    impressions = db.Column(db.Integer, nullable=False)
    clicks      = db.Column(db.Integer, nullable=False)
    spend       = db.Column(db.Integer, nullable=False)
    leads       = db.Column(db.Integer, nullable=False)
    conversions = db.Column(db.Integer, nullable=False)
    revenue     = db.Column(db.Integer, nullable=False)

    def __init__(self, id, budget, impressions, clicks, spend, leads, conversions, revenue):
        self.id          = id
        self.budget      = budget
        self.impressions = impressions
        self.clicks      = clicks
        self.spend       = spend
        self.leads       = leads
        self.conversions = conversions
        self.revenue     = revenue