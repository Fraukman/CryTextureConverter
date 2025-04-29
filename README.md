# CryTextureConverter

A simple and efficient desktop tool built with Python, PyQt5, and OpenCV to convert PBR texture maps from the **Metallic/Roughness** workflow to the **Specular/Glossiness** workflow, optimized for **CryEngine**.

## ✨ Features

- Load and preview multiple texture maps:
  - Diffuse
  - Ambient Occlusion
  - Opacity
  - Normal
  - Roughness
  - Metallic
  - Displacement
- Automatically generates:
  - Albedo (Diffuse × AO with Opacity as Alpha)
  - Gloss Map (from Roughness)
  - Specular Map (from Metallic)
  - Combined Normal+Gloss in Alpha
  - Displacement map copy
- Exports images with CryEngine-ready naming (`_albedo`, `_ddn`, `_ddna`, `_spec`, `_displ`)

## 🖥️ Running

You need Python 3.8+ and the following packages:

```
    pip install pyqt5 opencv-python
```

Then run:

```
    python main.py
```

## 🛠️ Building a Windows Executable

You can generate a standalone `.exe` using [PyInstaller](https://pyinstaller.org):

```
    pip install pyinstaller pyinstaller --noconfirm --onefile --windowed main.py
```
The `.exe` will be located in the `dist/` folder.


## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss.