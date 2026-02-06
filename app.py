from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')  # Nội dung code dán vào ô text
    [span_6](start_span)[span_7](start_span)target = data.get('type', '580VNX') # Lựa chọn dòng máy[span_6](end_span)[span_7](end_span)

    # [span_8](start_span)Xác định đường dẫn compiler tương ứng[span_8](end_span)
    compiler = "./580vnx/compiler_.py" if target == "580VNX" else "./880btg/compiler_.py"

    try:
        # [span_9](start_span)Thực thi compiler bằng cách truyền code qua stdin (tương tự < "$selected_file"[span_9](end_span))
        process = subprocess.Popen(
            ['python3', compiler, '-f', 'hex'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=code)

        if process.returncode == 0:
            return jsonify({"status": "success", "result": stdout})
        else:
            return jsonify({"status": "error", "message": stderr})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
