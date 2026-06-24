from app import create_app

# Create the app using the factory function
app = create_app()

if __name__ == '__main__':
    # debug=True means:
    # 1. The server restarts automatically when you save a file
    # 2. You see detailed error messages in the browser
    # Never use debug=True in production
    app.run(debug=True)