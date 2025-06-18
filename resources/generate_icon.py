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
    
    # Desenhar um cadeado estilizado em branco
    lock_color = (255, 255, 255, 255)  # Branco
    
    # Base do cadeado (retângulo arredondado simulado com várias formas)
    base_x1, base_y1, base_x2, base_y2 = 78, 108, 178, 208
    radius = 20
    
    # Desenhar retângulo principal
    draw.rectangle([base_x1 + radius, base_y1,
                   base_x2 - radius, base_y2], fill=lock_color)
    draw.rectangle([base_x1, base_y1 + radius,
                   base_x2, base_y2 - radius], fill=lock_color)
    
    # Adicionar cantos arredondados
    draw.ellipse([base_x1, base_y1,
                  base_x1 + radius*2, base_y1 + radius*2], fill=lock_color)
    draw.ellipse([base_x2 - radius*2, base_y1,
                  base_x2, base_y1 + radius*2], fill=lock_color)
    draw.ellipse([base_x1, base_y2 - radius*2,
                  base_x1 + radius*2, base_y2], fill=lock_color)
    draw.ellipse([base_x2 - radius*2, base_y2 - radius*2,
                  base_x2, base_y2], fill=lock_color)
    
    # Arco do cadeado
    arc_bounds = [68, 58, 188, 128]
    draw.arc(arc_bounds, start=0, end=180, fill=lock_color, width=20)
    
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