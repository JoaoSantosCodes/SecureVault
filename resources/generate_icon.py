from PIL import Image, ImageDraw, ImageFont
import os
from math import cos, sin, pi

def create_icon():
    # Criar uma imagem 256x256 com fundo transparente
    size = (256, 256)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Cores
    primary_color = (46, 204, 113)  # Verde esmeralda
    secondary_color = (255, 255, 255)  # Branco
    gradient_color = (39, 174, 96)  # Verde mais escuro para gradiente
    
    # Desenhar o escudo
    shield_margin = 20
    shield_width = size[0] - (2 * shield_margin)
    shield_height = size[1] - (2 * shield_margin)
    
    # Pontos do escudo (forma moderna)
    shield_points = [
        (shield_margin, shield_margin + shield_height * 0.2),  # Topo esquerdo
        (size[0] // 2, shield_margin),  # Topo centro
        (size[0] - shield_margin, shield_margin + shield_height * 0.2),  # Topo direito
        (size[0] - shield_margin, shield_margin + shield_height * 0.6),  # Meio direito
        (size[0] // 2, size[1] - shield_margin),  # Base
        (shield_margin, shield_margin + shield_height * 0.6),  # Meio esquerdo
    ]
    
    # Desenhar o escudo com gradiente
    for i in range(shield_height):
        y = shield_margin + i
        ratio = i / shield_height
        color = tuple(int(primary_color[j] + (gradient_color[j] - primary_color[j]) * ratio) for j in range(3))
        color = color + (255,)  # Adicionar canal alpha
        
        # Calcular pontos para esta linha do gradiente
        left_x = shield_margin
        right_x = size[0] - shield_margin
        
        if y < shield_margin + shield_height * 0.2:
            # Parte superior (triangular)
            progress = (y - shield_margin) / (shield_height * 0.2)
            left_x = shield_margin + (size[0] // 2 - shield_margin) * (1 - progress)
            right_x = (size[0] - shield_margin) - (size[0] // 2 - shield_margin) * (1 - progress)
        elif y > shield_margin + shield_height * 0.6:
            # Parte inferior (pontuda)
            progress = (y - (shield_margin + shield_height * 0.6)) / (shield_height * 0.4)
            left_x = shield_margin + (size[0] // 2 - shield_margin) * progress
            right_x = (size[0] - shield_margin) - (size[0] // 2 - shield_margin) * progress
        
        draw.line([(left_x, y), (right_x, y)], fill=color)
    
    # Desenhar as letras SV em branco com estilo moderno
    text_color = secondary_color
    
    # S estilizado
    s_width = 40
    s_height = 80
    s_x = 78
    s_y = 88
    s_thickness = 12
    
    # Curvas do S
    for i in range(3):
        curve_points = []
        if i == 0:  # Curva superior
            for t in range(0, 181, 5):
                x = s_x + s_width * cos(t * pi / 180) / 2
                y = s_y + s_height * sin(t * pi / 180) / 4
                curve_points.append((x, y))
        elif i == 1:  # Linha diagonal
            draw.line([(s_x + 5, s_y + s_height/4), 
                      (s_x + s_width - 5, s_y + s_height*3/4)], 
                     fill=text_color, width=s_thickness)
        else:  # Curva inferior
            for t in range(180, 361, 5):
                x = s_x + s_width * cos(t * pi / 180) / 2
                y = s_y + s_height * sin(t * pi / 180) / 4 + s_height/2
                curve_points.append((x, y))
        
        if i != 1:  # Desenhar curvas
            for j in range(len(curve_points)-1):
                draw.line([curve_points[j], curve_points[j+1]], 
                         fill=text_color, width=s_thickness)
    
    # V estilizado
    v_width = 50
    v_height = 60
    v_x = 138
    v_y = 98
    v_thickness = 12
    
    # Desenhar o V com linhas em ângulo
    draw.line([(v_x, v_y), (v_x + v_width/2, v_y + v_height)], 
              fill=text_color, width=v_thickness)
    draw.line([(v_x + v_width/2, v_y + v_height), (v_x + v_width, v_y)], 
              fill=text_color, width=v_thickness)
    
    # Salvar o ícone em vários tamanhos
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon_path = os.path.join('resources', 'images', 'securevault.ico')
    
    # Criar versões redimensionadas
    images = []
    for size in icon_sizes:
        resized = image.resize(size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Salvar como arquivo .ico
    images[0].save(
        icon_path,
        format='ICO',
        sizes=icon_sizes,
        append_images=images[1:]
    )
    
    # Salvar também como PNG para o README
    png_path = os.path.join('resources', 'images', 'securevault.png')
    image.save(png_path, format='PNG')
    
    print(f"Ícone gerado com sucesso em {icon_path}")
    print(f"PNG gerado com sucesso em {png_path}")

def create_shield_icon(size=(512, 512)):
    # Criar uma nova imagem com fundo transparente
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Cores
    shield_color = (0, 77, 38)  # Verde escuro
    text_color = (255, 255, 255)  # Branco
    
    # Dimensões do escudo
    width, height = size
    padding = width * 0.1
    shield_width = width - (2 * padding)
    shield_height = height - (2 * padding)
    
    # Desenhar o escudo (forma hexagonal)
    shield_points = [
        (padding + (shield_width * 0.2), padding),  # Topo esquerdo
        (padding + (shield_width * 0.8), padding),  # Topo direito
        (padding + shield_width, padding + (shield_height * 0.3)),  # Direita superior
        (padding + shield_width, padding + (shield_height * 0.7)),  # Direita inferior
        (padding + (shield_width * 0.5), padding + shield_height),  # Base
        (padding, padding + (shield_height * 0.7)),  # Esquerda inferior
        (padding, padding + (shield_height * 0.3)),  # Esquerda superior
    ]
    draw.polygon(shield_points, fill=shield_color)
    
    # Adicionar texto "SV"
    try:
        # Tentar carregar uma fonte do sistema
        font_size = int(min(width, height) * 0.4)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Se não encontrar a fonte, usar a fonte padrão
        font = ImageFont.load_default()
    
    text = "SV"
    # Calcular posição do texto para centralizar
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 - (height * 0.05)  # Pequeno ajuste para cima
    
    # Desenhar o texto
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    # Salvar as imagens
    if not os.path.exists('resources/images'):
        os.makedirs('resources/images')
        
    # Salvar como PNG
    image.save('resources/images/securevault.png', 'PNG')
    
    # Salvar como ICO
    image.save('resources/images/securevault.ico', 'ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

def convert_to_icon():
    # Abrir a imagem PNG existente
    img = Image.open('resources/images/securevault.png')
    
    # Converter para RGBA se não estiver nesse formato
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Criar o arquivo ICO com múltiplos tamanhos
    img.save('resources/images/securevault.ico', format='ICO', 
             sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print("Ícone gerado com sucesso!")

if __name__ == '__main__':
    create_icon()
    create_shield_icon()
    convert_to_icon() 