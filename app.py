import os
import time
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageFilter

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'static/uploads'
RESULTS_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Simulação de Banco de Dados em Memória
exams_db = []

def simulate_ai_heatmap(image_path, filename):
    """
    Simula a U-Net e o Grad-CAM (RNF-06).
    Gera um mapa de calor visual sobre a imagem original para parecer uma detecção.
    """
    # Abre a imagem original
    img = Image.open(image_path).convert('RGB')
    
    # Cria uma "máscara" simulada (apenas para efeito visual)
    # Na vida real, isso viria do modelo U-Net
    heatmap_data = np.random.rand(img.size[1], img.size[0])
    
    # Gera o mapa de calor usando Matplotlib
    plt.figure(figsize=(img.size[0]/100, img.size[1]/100), dpi=100)
    plt.imshow(img)
    plt.imshow(heatmap_data, cmap='jet', alpha=0.4) # Alpha define a transparência
    plt.axis('off')
    
    # Salva o resultado
    result_filename = f"result_{filename}"
    result_path = os.path.join(RESULTS_FOLDER, result_filename)
    plt.savefig(result_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return result_filename

@app.route('/')
def index():
    # Dashboard de Casos (RF-04)
    return render_template('index.html', exams=exams_db)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Upload e Fila de Processamento (RF-02)
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Simula o processamento assíncrono e rápido (RNF-02)
        time.sleep(1.5) 
        
        # Executa a "IA" (RF-03 e RF-05)
        result_filename = simulate_ai_heatmap(filepath, filename)
        
        # Salva no "banco"
        exam_data = {
            'id': len(exams_db) + 1,
            'original': filename,
            'result': result_filename,
            'patient': f"Paciente Anônimo {len(exams_db) + 1}", # RNF-04 (Privacidade)
            'status': 'Pendente de Revisão',
            'confidence': f"{np.random.randint(88, 99)}%" # Confiança simulada
        }
        exams_db.append(exam_data)
        
        return redirect(url_for('index'))

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)