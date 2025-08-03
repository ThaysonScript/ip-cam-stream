from models_ai.unets.unet_1x import UNet
import os, cv2, re, torch, shutil, subprocess, sys
from pathlib import Path
import numpy as np
import seaborn as sns
from ultralytics import YOLO


class AiProcess:
    def __init__(self):
        current_script_dir = Path(os.getcwd())
        parent_dir = current_script_dir.parent
        sys.path.append(str(parent_dir))
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Usando dispositivo: {device}")

        # --- Carregar Modelo UNet ---
        model_instance = UNet().to(device)
        unet_checkpoint_path_str = 'path_for/output/UNet_Best_IoU_weights.pth'

        if os.path.exists(unet_checkpoint_path_str):
            print(f"Carregando modelo UNet de: {unet_checkpoint_path_str}")
            unet_checkpoint = torch.load(unet_checkpoint_path_str, map_location=device)
            model_instance.load_state_dict(unet_checkpoint['state_dict'])
            print("Modelo UNet carregado com sucesso.")
        else:
            print(f"Erro: Checkpoint do modelo UNet não encontrado em {unet_checkpoint_path_str}.")
            print("Por favor, verifique se o caminho do modelo está correto ou treine o modelo primeiro.")
            exit()

        # --- Carregar Modelo YOLOv8 (Instanciado aqui, conforme solicitado) ---
        yolo_model_instance = YOLO('./models_ai/yolo/yolov8n.pt')
        print("Modelo YOLOv8 carregado com sucesso.")

        # --- Definir Caminho do Vídeo de Entrada ---
        input_video_to_process = 'path_for/video/recife.mp4'

        # Verificar se o vídeo de entrada existe
        if not os.path.exists(input_video_to_process):
            print(f"Erro: Vídeo de entrada '{input_video_to_process}' não encontrado.")
            print("Por favor, garanta que o vídeo exista no caminho especificado.")
            # Se o vídeo não existir e você quiser tentar criá-lo a partir de imagens,
            # você pode descomentar e ajustar a lógica abaixo, mas certifique-se
            # de que 'create_video' realmente crie o vídeo esperado em 'input_video_to_process'.
            # if not create_video():
            #     print(f"Falha ao criar o vídeo '{input_video_to_process}'.")
            #     exit()
            exit()

        output_videos_dir = "."
        Path(output_videos_dir).mkdir(parents=True, exist_ok=True)

        print(f"\nIniciando processamento combinado (UNet e YOLO) para o vídeo '{input_video_to_process}'...")
        processed_video_path = self.process_video(
            video_path=input_video_to_process,
            model=model_instance,
            yolo_model=yolo_model_instance, # Passa o modelo YOLO instanciado
            iou_calculator_func=self.calculate_iou, # Passa a função calculate_iou importada
            device=device,
            output_dir=output_videos_dir
        )

        if processed_video_path:
            print(f"Processamento combinado concluído. Vídeo de saída: {processed_video_path}")
        else:
            print(f"O processamento combinado falhou para '{input_video_to_process}'.")
    
    
    def calculate_iou(self, box1, mask):
        x1, y1, x2, y2 = [int(coord) for coord in box1[:4]]
        box_area = (x2 - x1) * (y2 - y1)

        if box_area == 0:
            return 0.0

        box_mask = np.zeros_like(mask, dtype=np.uint8)
        cv2.rectangle(box_mask, (x1, y1), (x2, y2), 1, -1)
        intersection = np.sum((box_mask > 0) & (mask > 0))
        union = np.sum((box_mask > 0) | (mask > 0))

        if union == 0:
            return 0.0
        return intersection / union


    def reencode_video_ffmpeg(self, input_path, output_path):
        """
        Re-codifica um vídeo usando ffmpeg para garantir compatibilidade.
        Assume que ffmpeg.exe está acessível no caminho especificado.
        """
        print('Processando ffmpeg...')
        ffmpeg_path = r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin\ffmpeg.exe"
        command = [ffmpeg_path, '-y', '-i', input_path, '-c:v', 'libx264', '-profile:v', 'baseline',
                '-level', '3.0', '-pix_fmt', 'yuv420p', '-c:a', 'aac', output_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print('ffmpeg terminou com sucesso.')
            
        except subprocess.CalledProcessError as e:
            print(f"Erro durante o processamento com ffmpeg: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            raise


    def ordena_natural(self, s):
        """
        Ordena strings naturalmente, tratando números dentro das strings corretamente.
        """
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('(\d+)', s)]


    def create_video(self):
        """
        Cria um vídeo a partir de uma sequência de imagens.
        """
        folder_path = 'path_for/datasets/dataset_recife/test-seg/images'
        output_video_path_str = 'path_for/interface/videos/testes_original.mp4'
        output_video_path = Path(output_video_path_str)
        output_video_path.parent.mkdir(parents=True, exist_ok=True)

        frame_rate = 10  # FPS

        if not os.path.exists(folder_path):
            print(f"Erro: Pasta de imagens de origem '{folder_path}' não encontrada.")
            return False

        images = sorted(
        [img for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))],
            key=self.ordena_natural
        )

        if not images:
            print(f"Nenhuma imagem encontrada em {folder_path} para criar o vídeo.")
            return False

        frame_example_path = os.path.join(folder_path, images[0])
        frame_example = cv2.imread(frame_example_path)
        
        if frame_example is None:
            print(f"Não foi possível ler a primeira imagem: {frame_example_path}")
            return False
        
        height, width, _ = frame_example.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_video_path_str, fourcc, frame_rate, (width, height))

        if not video.isOpened():
            print(f"Erro: Não foi possível abrir o gravador de vídeo para {output_video_path_str}")
            return False

        for image_name in images:
            frame_path = os.path.join(folder_path, image_name)
            frame = cv2.imread(frame_path)
            
            if frame is not None:
                video.write(frame)
            else:
                print(f"Aviso: Não foi possível ler a imagem {frame_path}. Pulando.")

        video.release()
        print(f'Vídeo salvo em: {output_video_path_str}')
        return True


    def give_color_to_annotation(self, annotation: np.ndarray) -> np.ndarray:
        """
        Converte uma máscara de anotação 2D em uma imagem RGB colorida baseada nas classes.
        """
        class_names = ["Water", "Land"]
        colors = sns.color_palette(None, len(class_names))

        seg_img = np.zeros((*annotation.shape, 3), dtype=np.float32)
        for c in range(len(class_names)):
            segc = annotation == c
            for i_color_channel in range(3):
                seg_img[:, :, i_color_channel] += segc * (colors[c][i_color_channel] * 255.0)

        return seg_img.astype(np.uint8)


    def process_video(self,
        video_path: str,
        model: torch.nn.Module,
        yolo_model: YOLO, # Tipo YOLO agora é possível devido à importação
        iou_calculator_func: callable, # Função calculate_iou importada
        device: torch.device,
        output_dir: str,
        confidence_threshold: float = 0.4, # Limiar de confiança para detecção de pessoas
        iou_threshold: float = 0.1 # Limiar de IoU para considerar uma pessoa "na água"
    ):
        """
        Função Principal de Processamento de Vídeo (Modificada para usar YOLO e IoU)

        Processa um único vídeo, realizando segmentação de água e detecção/rastreamento de pessoas,
        e determina se as pessoas detectadas estão na água.
        Retorna o caminho do vídeo de saída.
        """
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Erro: Não foi possível abrir o arquivo de vídeo {video_path}")
            return None

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # O modelo UNet frequentemente requer dimensões de entrada específicas,
        # garantindo que sejam múltiplos de 16 (ou outro valor específico dependendo da arquitetura UNet)
        unet_input_width = width - (width % 16)
        unet_input_height = height - (height % 16)
        print(f"Redimensionando quadros para UNet para: ({unet_input_width}, {unet_input_height})")

        # Define o caminho do vídeo de saída
        output_video_file_name = f"processed_combined_{Path(video_path).name}"
        output_video_file_path = output_dir_path / output_video_file_name

        # Para visualização, combinaremos o quadro original, a sobreposição segmentada,
        # e os resultados da detecção. A largura do vídeo de saída será três vezes a largura original.
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(str(output_video_file_path), fourcc, fps, (width * 3, height))

        if not out_video.isOpened():
            print(f"Erro: Não foi possível abrir o gravador de vídeo para {output_video_file_path}")
            return None

        model.eval() # Define o modelo UNet para o modo de avaliação

        # Variáveis para persistência do rastreamento YOLO
        previous_tracked_boxes = []

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fim do vídeo ou erro ao ler o quadro.")
                break

            frame_count += 1
            if frame_count % 10 != 0:
                continue

            else:
                print(f"Processando quadro {frame_count}...")

            # --- Segmentação UNet ---
            # Redimensiona o quadro para o processamento UNet
            frame_for_unet = cv2.resize(frame, (unet_input_width, unet_input_height))
            current_frame_rgb_unet = cv2.cvtColor(frame_for_unet, cv2.COLOR_BGR2RGB)
            current_tensor = torch.from_numpy(current_frame_rgb_unet.transpose(2, 0, 1)).float().unsqueeze(0).to(device)

            with torch.no_grad():
                prediction = model(current_tensor)
                # A máscara de água será 0 (água) e 1 (terra)
                current_mask_predicted = (torch.sigmoid(prediction) > 0.5).cpu().numpy().squeeze().astype(np.uint8)

            # Redimensiona a máscara de volta para as dimensões do quadro original para overlay/IoU
            current_mask_predicted_resized = cv2.resize(current_mask_predicted, (width, height), interpolation=cv2.INTER_NEAREST)

            # Colore a máscara de segmentação para visualização
            seg_colored = self.give_color_to_annotation(current_mask_predicted_resized)
            # Cria uma sobreposição para visualização
            segmentation_overlay = cv2.addWeighted(frame, 0.6, seg_colored, 0.4, 0)

            # Criar uma máscara binária onde 1 é água e 0 é terra (assumindo que 0 na máscara predita é água)
            binary_water_mask = (current_mask_predicted_resized == 0).astype(np.uint8)

            # --- Detecção e Rastreamento de Objetos YOLOv8 ---
            # YOLO opera no tamanho do quadro original ou redimensiona internamente
            yolo_results = yolo_model.track(frame, persist=True, verbose=False) # yolo_model é passado como parâmetro

            # Get tracking data
            # Check if results[0].boxes.data exists and is not empty
            if yolo_results and yolo_results[0].boxes.data is not None:
                tracked_boxes = yolo_results[0].boxes.data.cpu().numpy()
                previous_tracked_boxes = tracked_boxes # Update for persistence
            else:
                tracked_boxes = previous_tracked_boxes # Use previous if no new detections

            # Create a copy of the original frame to draw detections on
            detection_frame = frame.copy()

            # Process detected objects (people only)
            for box in tracked_boxes:
                # Boxes can have 6 (no track_id) or 7 (with track_id) elements
                if len(box) >= 6:
                    x1, y1, x2, y2, score, class_id = box[:6]
                    track_id = box[6] if len(box) == 7 else -1 # Assign -1 if no track_id

                    # Check if the class is 'person' (class ID 0 for COCO dataset) and confidence is sufficient
                    if int(class_id) == 0 and score >= confidence_threshold:
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        # Determine if the person is in the water
                        person_box = [x1, y1, x2, y2]
                        # Usa a função calculate_iou passada como parâmetro
                        iou_with_water = iou_calculator_func(person_box, binary_water_mask)

                        text_label = f'ID: {int(track_id)}' if track_id != -1 else ''

                        if iou_with_water > iou_threshold:
                            bgr_color = (255, 0, 0)  # Vermelho para "Na Água"
                            text_label += ' (Na Água)'
                        else:
                            bgr_color = (0, 255, 0)  # Verde para "Fora da Água"
                            text_label += ' (Fora da Água)'

                        cv2.rectangle(detection_frame, (x1, y1), (x2, y2), bgr_color, 2)
                        cv2.putText(detection_frame, text_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, bgr_color, 2)

            # --- Combine all three visualizations into one frame ---
            combined = np.hstack([
                frame,                   # Quadro original
                segmentation_overlay,    # Quadro com sobreposição de segmentação
                detection_frame          # Quadro com detecções de pessoas e status da água
            ])
            out_video.write(combined)

        out_video.release()
        cap.release()
        print(f"Vídeo processado (segmentação e detecção) salvo em: {output_video_file_path}")

        return str(output_video_file_path)