"""
Hariom Solar Website - Flask Application
A complete solar energy website with HTML, CSS, and JavaScript frontend
"""

from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='static', template_folder='.')

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['DEBUG'] = True


@app.route('/')
def index():
    """
    Main route - serves the homepage
    """
    return send_from_directory('.', 'index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    """
    Serve static files (CSS, JS, images)
    """
    return send_from_directory('static', filename)


@app.route('/api/contact', methods=['POST'])
def contact():
    """
    API endpoint for contact form submissions
    This is a placeholder - add your email service integration here
    """
    from flask import request
    
    data = request.get_json()
    
    # Validate data
    if not data or 'email' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    # Here you would typically:
    # 1. Validate the data
    # 2. Send an email
    # 3. Store in database
    # 4. Send confirmation email
    
    print(f"Contact form submission: {data}")
    
    return jsonify({
        'success': True,
        'message': 'Thank you for your interest! We will contact you soon.'
    }), 200


@app.route('/api/quote', methods=['POST'])
def get_quote():
    """
    API endpoint for solar quote requests
    This is a placeholder - add your quote calculation logic here
    """
    from flask import request
    
    data = request.get_json()
    
    # Validate data
    required_fields = ['name', 'email', 'phone', 'address']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Here you would typically:
    # 1. Calculate solar panel requirements
    # 2. Estimate costs
    # 3. Store in database
    # 4. Send quote via email
    
    print(f"Quote request: {data}")
    
    return jsonify({
        'success': True,
        'message': 'Quote request received! Our team will contact you within 24 hours.',
        'quote_id': 'QUOTE-2026-001'
    }), 200


@app.route('/api/calculator', methods=['POST'])
def solar_calculator():
    """
    Solar savings calculator endpoint
    Calculates potential savings based on user input
    """
    from flask import request
    
    data = request.get_json()
    
    # Get user inputs
    monthly_bill = float(data.get('monthly_bill', 0))
    home_size = int(data.get('home_size', 0))
    location = data.get('location', 'Unknown')
    
    # Simple calculation (this should be more sophisticated in production)
    average_cost_per_kwh = 0.13
    monthly_usage = monthly_bill / average_cost_per_kwh
    annual_usage = monthly_usage * 12
    
    # Estimate system size (rough approximation)
    system_size_kw = annual_usage / 1200  # kWh per year / 1200 hours
    
    # Cost estimates
    cost_per_watt = 3.00
    system_cost = system_size_kw * 1000 * cost_per_watt
    
    # Savings (assuming 70% offset)
    annual_savings = monthly_bill * 12 * 0.7
    roi_years = system_cost / annual_savings
    
    # 25-year savings
    lifetime_savings = annual_savings * 25 - system_cost
    
    return jsonify({
        'success': True,
        'results': {
            'annual_usage_kwh': round(annual_usage, 2),
            'recommended_system_size_kw': round(system_size_kw, 2),
            'estimated_system_cost': round(system_cost, 2),
            'annual_savings': round(annual_savings, 2),
            'payback_period_years': round(roi_years, 1),
            'lifetime_savings_25_years': round(lifetime_savings, 2),
            'co2_offset_lbs_per_year': round(annual_usage * 0.7 * 0.92, 2)
        }
    }), 200


@app.errorhandler(404)
def not_found(e):
    """
    404 error handler
    """
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """
    500 error handler
    """
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check if static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')
        print("Created 'static' directory")
    
    # Run the application
    print("=" * 60)
    print("Hariom Solar Website - Flask Application")
    print("=" * 60)
    print("\nStarting development server...")
    print("\nAccess the website at: http://localhost:5000")
    print("\nAPI Endpoints available:")
    print("  - POST /api/contact    - Contact form submission")
    print("  - POST /api/quote      - Request solar quote")
    print("  - POST /api/calculator - Solar savings calculator")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
