# utils/validators.py
# Responsibility: validate input data before it enters the system

def validate_campaign_data(data):
    errors = []

    required_fields = ["name", "budget", "impressions", 
                   "clicks", "spend", "leads", 
                   "conversions", "revenue"]

    # check all required fields exist
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # check numeric fields are positive
    numeric_fields = ["budget", "impressions", "clicks", 
                      "spend", "leads", "conversions", "revenue"]
    
    for field in numeric_fields:
        if field in data:
            if not isinstance(data[field], (int, float)):
                errors.append(f"{field} must be a number")
            elif data[field] < 0:
                errors.append(f"{field} cannot be negative")

    if errors:
        return {"valid": False, "errors": errors}
    
    return {"valid": True, "errors": []}