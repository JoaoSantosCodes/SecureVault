from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Criar uma imagem 256x256 com fundo transparente
    size = (256, 256)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Desenhar um círculo verde escuro como fundo
    circle_color = (34, 139, 34, 255)  # Verde escuro
    circle_bounds = [20, 20, 236, 236]  # Margens de 20px
    draw.ellipse(circle_bounds, fill=circle_color)
    
    # Desenhar as letras SV em branco
    text_color = (255, 255, 255, 255)  # Branco
    
    # Criar fonte para o texto (usando um retângulo como substituto da fonte)
    # S
    s_width = 60
    s_height = 100
    s_x = 68
    s_y = 78
    
    # Parte superior do S
    draw.rectangle([s_x, s_y, s_x + s_width, s_y + 20], fill=text_color)
    # Parte vertical superior
    draw.rectangle([s_x, s_y, s_x + 20, s_y + s_height//2], fill=text_color)
    # Parte do meio
    draw.rectangle([s_x, s_y + (s_height//2 - 10), s_x + s_width, s_y + (s_height//2 + 10)], fill=text_color)
    # Parte vertical inferior
    draw.rectangle([s_x + s_width - 20, s_y + s_height//2, s_x + s_width, s_y + s_height], fill=text_color)
    # Parte inferior
    draw.rectangle([s_x, s_y + s_height - 20, s_x + s_width, s_y + s_height], fill=text_color)
    
    # V
    v_width = 60
    v_height = 100
    v_x = 148
    v_y = 78
    
    # Desenhar o V usando linhas grossas
    points_left = [(v_x, v_y), (v_x + v_width//2, v_y + v_height)]
    points_right = [(v_x + v_width//2, v_y + v_height), (v_x + v_width, v_y)]
    
    # Desenhar linhas grossas para formar o V
    for i in range(20):  # Espessura da linha
        offset = i - 10
        draw.line([(p[0] + offset, p[1]) for p in points_left], fill=text_color, width=2)
        draw.line([(p[0] + offset, p[1]) for p in points_right], fill=text_color, width=2)
    
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

if __name__ == '__main__':
    create_icon() 