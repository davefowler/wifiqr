from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code = None
    network_info = {}
    
    if request.method == 'POST':
        ssid = request.form.get('ssid', '')
        password = request.form.get('password', '')
        show_password = request.form.get('show_password') == 'on'
        
        # Generate WiFi QR code
        wifi_string = f'WIFI:T:WPA;S:{ssid};P:{password};;'
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(wifi_string)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert image to base64 for displaying
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code = base64.b64encode(buffered.getvalue()).decode()
        
        network_info = {
            'ssid': ssid,
            'password': password if show_password else '********',
            'show_password': show_password
        }
    
    return render_template('index.html', qr_code=qr_code, network_info=network_info)

if __name__ == '__main__':
    app.run(debug=True)
