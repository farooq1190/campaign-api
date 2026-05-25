def calculate_ctr(campaign):
        try:
            if campaign.impressions > 0:
                return round((campaign.clicks / campaign.impressions) * 100, 2)
            else:
                return "No impression Yet"
        except TypeError:
            return "Error: Invalid data tyype"
    
    
    
def calculate_cpl(campaign):
        try:
            if campaign.leads > 0:
                cpl = campaign.spend / campaign.leads
                return round(cpl, 2)
            else:
                return "No leads generated."
        except TypeError:
            return "Error: Invalid data type for spend"

def calculate_roas(campaign):
        try:
            if campaign.spend > 0:
                roas = campaign.revenue / campaign.spend
                return round(roas, 2)
            else:
                return "No spend, ROAS cannot be calculated."
        except TypeError:
            return "Error: Invalid data type for revenue or spend."
    
    
def budget_remaining(campaign):
     return campaign.budget - campaign.spend

def campaign_report(campaign):
        try:
            report = {
                "id": campaign.id,
                "CTR": calculate_ctr(campaign),
                "Budget Remaining": budget_remaining(campaign),
                "Status": "On Track" if campaign.spend <= campaign.budget else "Over Budget",
                "Leads": campaign.leads,
                "Conversions": campaign.conversions,
                "Revenue": campaign.revenue,
                "CPL": calculate_cpl(campaign),
                "ROAS": calculate_roas(campaign)
            }
            return report
        except Exception as e:
             return {"error": str(e)}
        