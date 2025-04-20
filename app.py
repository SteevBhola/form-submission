from flask import Flask, render_template, request
from flask_mail import Mail, Message
from xhtml2pdf import pisa
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'steevbhola68@gmail.com'      # Your Gmail
app.config['MAIL_PASSWORD'] = 'dmql ishh hdqj iwye'           # App Password

mail = Mail(app)

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    data = {k: request.form[k] for k in request.form}
    file = request.files['document']

    # Save uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Create PDF content
    pdf_html = f"""
    <h2>Company Details</h2>
    <p><strong>Company:</strong> {data['company_name']}</p>
    <p><strong>Address:</strong> {data['address']}</p>
    <p><strong>Mobile:</strong> {data['mobile']}</p>
    <p><strong>Telephone:</strong> {data['telephone']}</p>
    <p><strong>Customer Type:</strong> {data['customer_type']}</p>
    <p><strong>Discount:</strong> {data['discount_structure']}</p>
    <p><strong>Contact Person:</strong> {data['contact_person']}</p>
    <p><strong>GSTIN:</strong> {data['gstin']}</p>
    <p><strong>PAN:</strong> {data['pan']}</p>
    """

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'form.pdf')
    with open(pdf_path, "wb") as pdf_file:
        pisa.CreatePDF(pdf_html, dest=pdf_file)

    # Send Email with attachments
    msg = Message("New Company Form Submitted",
                  sender="steevbhola68@gmail.com",
                  recipients=["steevbhola68@gmail.com"])
    msg.body = "A new form has been submitted. Please check the attachments."

    with app.open_resource(pdf_path) as pdf:
        msg.attach("form.pdf", "application/pdf", pdf.read())

    with app.open_resource(file_path) as doc:
        msg.attach(file.filename, file.content_type, doc.read())

    mail.send(msg)

    return "Form submitted, PDF generated and email sent!"

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
