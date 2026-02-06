from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Đảm bảo các thư mục compiler tồn tại
# Cấu trúc: ./580vnx/compiler_.py và ./880btg/compiler_.py

@app.route('/')
def index():
    # Trả về file HTML giao diện trắng xanh 2 ô của bạn
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    source_code = data.get('code', '')  # Mã lấy từ ô "MÃ NGUỒN (INPUT)"
    target_core = data.get('type', '580VNX') # Loại Core chọn từ Select box

    # Xác định đường dẫn file compiler tương ứng
    if target_core == "580VNX":
        compiler_path = "./580vnx/compiler_.py"
    else:
        compiler_path = "./880btg/compiler_.py"

    # Kiểm tra xem file compiler có tồn tại không để tránh lỗi server
    if not os.path.exists(compiler_path):
        return jsonify({
            "status": "error", 
            "message": f"Không tìm thấy file compiler tại {compiler_path}"
        })

    try:
        # Chạy compiler bằng Python3
        # Truyền source_code trực tiếp vào stdin (giống như lệnh < trong Bash)
        process = subprocess.Popen(
            ['python3', compiler_path, '-f', 'hex'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Gửi mã nguồn vào và nhận kết quả đầu ra
        stdout, stderr = process.communicate(input=source_code)

        if process.returncode == 0:
            # Nếu thành công, trả về nội dung đã biên dịch cho ô OUTPUT
            return jsonify({"status": "success", "result": stdout.strip()})
        else:
            # Nếu compiler báo lỗi (sai cú pháp...), trả về lỗi cho ô OUTPUT
            return jsonify({"status": "error", "message": stderr.strip()})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Chạy server tại cổng 5000
    print("--- Server đang chạy tại http://127.0.0.1:5000 ---")
    app.run(host='0.0.0.0', port=5000, debug=True)
