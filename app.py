from flask import Flask
from flask_cors import CORS
from services.accounts_service import accounts_bp
from services.loans_service import loans_bp
from services.transactions_service import transactions_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register service blueprints
    app.register_blueprint(accounts_bp, url_prefix='/api')
    app.register_blueprint(loans_bp, url_prefix='/api')
    app.register_blueprint(transactions_bp, url_prefix='/api')
    
    @app.route('/')
    def health_check():
        return {'status': 'Banking System API is running', 'services': ['accounts', 'loans', 'transactions']}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
