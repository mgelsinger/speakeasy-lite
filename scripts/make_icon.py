import os
from PIL import Image, ImageDraw


def make_ico(path):
    sizes = [16, 32, 48, 64, 128, 256]
    frames = []
    for s in sizes:
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        m = max(1, s // 8)
        ImageDraw.Draw(img).ellipse([m, m, s - m, s - m], fill=(50, 180, 50, 255))
        frames.append(img)
    frames[0].save(path, format="ICO", append_images=frames[1:])
    print(f"Icon saved: {path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "app", "assets", "icon.ico")
    make_ico(os.path.abspath(out))
