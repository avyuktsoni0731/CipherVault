from app import app
import os

if __name__ == "__main__":
    # app.run(debug=True, port=8080)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)