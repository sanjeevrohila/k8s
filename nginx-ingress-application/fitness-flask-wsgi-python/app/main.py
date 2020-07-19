from flask import Flask, render_template
import socket
app = Flask(__name__)


@app.route("/")
def home():
    host_name, host_ip = None, None
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP") 

    return render_template(
        "home.html",
        hostname=host_name,
        ipaddress=host_ip)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
