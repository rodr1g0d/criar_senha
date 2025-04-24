import secrets
import string

# Gera uma senha forte com 20 caracteres import as libs e seja feliz
alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for _ in range(20))
password

print(password)

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instalação Automática MDM</title>
    <style>
        body { 
            font-family: Arial; 
            text-align: center; 
            padding: 20px; 
            background-color: #f5f5f5;
        }
        .progress {
            display: block;
            width: 100%;
            max-width: 400px;
            height: 10px;
            margin: 20px auto;
            background-color: #ddd;
            border-radius: 5px;
        }
        .progress-bar {
            height: 100%;
            width: 0;
            background-color: #4CAF50;
            border-radius: 5px;
            transition: width 0.3s;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instalando Cashly MDM</h1>
        <p>A instalação começará automaticamente em 2 segundos...</p>
        <div class="progress">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        <p id="status">Preparando download...</p>
    </div>

    <script>
        // Simular progresso
        let progress = 0;
        const progressBar = document.getElementById('progressBar');
        const status = document.getElementById('status');
        
        const interval = setInterval(() => {
            progress += 5;
            progressBar.style.width = progress + '%';
            
            if (progress === 30) {
                status.textContent = "Baixando aplicativo...";
            } else if (progress === 60) {
                status.textContent = "Preparando instalação...";
            } else if (progress === 90) {
                status.textContent = "Finalizando...";
            } else if (progress >= 100) {
                clearInterval(interval);
                status.textContent = "Iniciando instalação!";
                // Iniciar download automaticamente após 2 segundos
                setTimeout(() => {
                    window.location.href = "/mdm.apk";
                }, 500);
            }
        }, 100);

        // Iniciar download automaticamente após 2 segundos
        setTimeout(() => {
            window.location.href = "/mdm.apk";
        }, 2000);
    </script>
</body>
</html>
