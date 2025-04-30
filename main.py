import os
import sys
import cv2
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

class ImageLoaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.image_formats = "Imagens (*.png *.jpg *.bmp *.tiff *.tga)"

        self.setWindowTitle("Cry Texture converter")
        self.resize(600, 600)

        # Variáveis para armazenar as imagens
        self.diffuse_img = None
        self.ao_img = None
        self.opacity_img = None
        self.normal_img = None
        self.roughness_img = None
        self.metallic_img = None
        self.displacement_img = None
        self.orm_img = None

        layout = QVBoxLayout()

        # ---- Diffuse Load ---- #
        diffuse_layout = QHBoxLayout()
        self.load_diffuse_btn = QPushButton("Load Diffuse")
        self.load_diffuse_btn.clicked.connect(self.load_diffuse)
        diffuse_layout.addWidget(self.load_diffuse_btn)

        self.remove_diffuse_button = QPushButton("🗑️", self)
        self.remove_diffuse_button.clicked.connect(self.remove_diffuse)
        self.remove_diffuse_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        diffuse_layout.addWidget(self.remove_diffuse_button)
        layout.addLayout(diffuse_layout)

        # ---- AO Load ---- #
        ao_layout = QHBoxLayout()
        self.load_ao_btn = QPushButton("Load AO")
        self.load_ao_btn.clicked.connect(self.load_ao)
        ao_layout.addWidget(self.load_ao_btn)

        self.remove_ao_button = QPushButton("🗑️", self)
        self.remove_ao_button.clicked.connect(self.remove_ao)
        self.remove_ao_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ao_layout.addWidget(self.remove_ao_button)
        layout.addLayout(ao_layout)  

        # ---- Opacity Load ---- #
        opacity_layout = QHBoxLayout()
        self.load_opacity_btn = QPushButton("Load Opacity")
        self.load_opacity_btn.clicked.connect(self.load_opacity)
        opacity_layout.addWidget(self.load_opacity_btn)

        self.remove_opacity_button = QPushButton("🗑️", self)
        self.remove_opacity_button.clicked.connect(self.remove_opacity)
        self.remove_opacity_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        opacity_layout.addWidget(self.remove_opacity_button)
        layout.addLayout(opacity_layout)       
       
        # ---- Normal Load ---- #
        normal_layout = QHBoxLayout()
        self.load_normal_btn = QPushButton("Load Normal")
        self.load_normal_btn.clicked.connect(self.load_normal)
        normal_layout.addWidget(self.load_normal_btn)

        self.remove_normal_button = QPushButton("🗑️", self)
        self.remove_normal_button.clicked.connect(self.remove_normal)
        self.remove_normal_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        normal_layout.addWidget(self.remove_normal_button)
        layout.addLayout(normal_layout)    

        # ---- Roughness Load ---- #
        roughness_layout = QHBoxLayout()
        self.load_roughness_btn = QPushButton("Load Roughness")
        self.load_roughness_btn.clicked.connect(self.load_roughness)
        roughness_layout.addWidget(self.load_roughness_btn)

        self.remove_roughness_button = QPushButton("🗑️", self)
        self.remove_roughness_button.clicked.connect(self.remove_roughness)
        self.remove_roughness_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        roughness_layout.addWidget(self.remove_roughness_button)
        layout.addLayout(roughness_layout)    

        # ---- Metallic Load ---- #
        metallic_layout = QHBoxLayout()
        self.load_metallic_btn = QPushButton("Load Metallic")
        self.load_metallic_btn.clicked.connect(self.load_metallic)
        metallic_layout.addWidget(self.load_metallic_btn)

        self.remove_metallic_button = QPushButton("🗑️", self)
        self.remove_metallic_button.clicked.connect(self.remove_metallic)
        self.remove_metallic_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        metallic_layout.addWidget(self.remove_metallic_button)
        layout.addLayout(metallic_layout)            


        # ---- Displacement Load ---- #
        displacement_layout = QHBoxLayout()
        self.load_displacement_btn = QPushButton("Load Displacement")
        self.load_displacement_btn.clicked.connect(self.load_displacement)
        displacement_layout.addWidget(self.load_displacement_btn)

        self.remove_displacement_button = QPushButton("🗑️", self)
        self.remove_displacement_button.clicked.connect(self.remove_displacement)
        self.remove_displacement_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        displacement_layout.addWidget(self.remove_displacement_button)
        layout.addLayout(displacement_layout)      

        self.load_ORM_btn = QPushButton("Load ORM")
        self.load_ORM_btn.clicked.connect(self.load_orm)
        layout.addWidget(self.load_ORM_btn)

        self.auto_load_btn = QPushButton("Auto Load Folder 📂")
        self.auto_load_btn.clicked.connect(self.auto_load_from_folder)
        layout.addWidget(self.auto_load_btn)
        
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_output)
        layout.addWidget(self.generate_button)

        self.status_label = QLabel("Load the texture maps and click on generate")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)  # Adiciona o status ao layout

        self.reset_button = QPushButton("Reset All 🗑️")
        self.reset_button.clicked.connect(self.remove_all)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def load_image_cv_compat(self, file_path):
        try:
            img = cv2.imread(file_path)
            if img is not None:
                return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception:
            pass

        try:
            pil_img = Image.open(file_path).convert("RGB")
            return np.array(pil_img)
        except Exception as e:
            print(f"failed to load image: {e}")
            return None

   
    def load_diffuse(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Diffuse", "", self.image_formats)       
        self.gen_albedo(file_name)
    
    def gen_albedo(self,file_path):
        if file_path:
            self.diffuse_img = self.load_image_cv_compat(file_path)
            if(self.diffuse_img is not None):
                self.load_diffuse_btn.setText("Diffuse Loaded ✅")
                self.load_diffuse_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")
                print("Diffuse loaded.")

    def load_ao(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open AO", "", self.image_formats)
        self.gen_ao(file_name)

    def gen_ao(self,file_path):
        if file_path:
            self.ao_img = self.load_image_cv_compat(file_path)
            if(self.ao_img is not None):
                self.load_ao_btn.setText("AO Loaded ✅")
                self.load_ao_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")
                print("AO loaded.")

    def load_opacity(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Opacity", "", self.image_formats)
        self.gen_opacity(file_name)

    def gen_opacity(self, file_path):
        if file_path:
            self.opacity_img = self.load_image_cv_compat(file_path)
            if(self.opacity_img is not None):
                self.load_opacity_btn.setText("Opacity Loaded ✅")
                self.load_opacity_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")
                print("Opacity loaded.")

    def load_normal(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Normal", "", self.image_formats)
        self.gen_normal(file_name)

    def gen_normal(self,file_path):
        if file_path:
            self.normal_img = self.load_image_cv_compat(file_path)
            if(self.normal_img is not None):
                self.load_normal_btn.setText("Normal Loaded ✅")
                self.load_normal_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")
                print("Normal loaded.")

    def load_roughness(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Roughness", "", self.image_formats)
        self.gen_roughness(file_name)

    def gen_roughness(self, file_path):
        if file_path:
            self.roughness_img = self.load_image_cv_compat(file_path)
            if(self.roughness_img is not None):
                self.load_roughness_btn.setText("Roughness Loaded ✅")
                self.load_roughness_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")
                print("Roughness loaded.")

    def load_metallic(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Metallic", "", self.image_formats)
        self.gen_metallic(file_name)

    def gen_metallic(self,file_path):
        if file_path:
            self.metallic_img = self.load_image_cv_compat(file_path)
            if(self.metallic_img is not None):
                self.load_metallic_btn.setText("Metallic Loaded ✅")
                self.load_metallic_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")
                print("Metallic loaded.")

    def load_displacement(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Displacement", "", self.image_formats)
        self.gen_displacement(file_name)

    def gen_displacement(self,file_path):
        if file_path:
            self.displacement_img = self.load_image_cv_compat(file_path)
            if(self.displacement_img is not None):
                self.load_displacement_btn.setText("Displacement Loaded ✅")
                self.load_displacement_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")
                print("Displacement loaded.")
    
    def load_orm(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load ORM", "", self.image_formats)
        self.gen_orm(file_name)

    def gen_orm(self, file_path):
        if file_path:
            self.orm_img = self.load_image_cv_compat(file_path)
            if self.orm_img is not None:
                r, g, b = cv2.split(self.orm_img)
                
                self.ao_img = cv2.merge([r, r, r])         # AO no canal R
                self.roughness_img = cv2.merge([g, g, g])  # Roughness no canal G
                self.metallic_img = cv2.merge([b, b, b])   # Metallic no canal B
                
                self.load_metallic_btn.setText("Metallic Loaded ✅")
                self.load_metallic_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")

                self.load_roughness_btn.setText("Roughness Loaded ✅")
                self.load_roughness_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")

                self.load_ao_btn.setText("AO Loaded ✅")
                self.load_ao_btn.setStyleSheet("background-color: lightgreen; font-weight: bold; color: darkgreen;")

                print("ORM loaded and splited with success.")

    def remove_diffuse(self):
        self.diffuse_img = None  # Remove a imagem do QLabel
        self.load_diffuse_btn.setText("Load Diffuse")
        self.load_diffuse_btn.setStyleSheet("color: black; font-weight: regular;")

    def remove_ao(self):
        self.ao_img = None  # Remove a imagem do QLabel
        self.load_ao_btn.setText("Load AO")
        self.load_ao_btn.setStyleSheet("color: black; font-weight: regular;")

    def remove_normal(self):
        self.normal_img = None  # Remove a imagem do QLabel
        self.load_normal_btn.setText("Load Normal")
        self.load_normal_btn.setStyleSheet("color: black; font-weight: regular;")

    def remove_opacity(self):
        self.opacity_img = None  # Remove a imagem do QLabel
        self.load_opacity_btn.setText("Load Opacity")
        self.load_opacity_btn.setStyleSheet("color: black; font-weight: regular;")

    def remove_roughness(self):
        self.roughness_img = None  # Remove a imagem do QLabel
        self.load_roughness_btn.setText("Load Roughness")
        self.load_roughness_btn.setStyleSheet("color: black; font-weight: regular;")

    def remove_metallic(self):
        self.metallic_img = None  # Remove a imagem do QLabel
        self.load_metallic_btn.setText("Load Metallic")
        self.load_metallic_btn.setStyleSheet("color: black; font-weight: regular;")

    def remove_displacement(self):
        self.displacement_img = None  # Remove a imagem do QLabel
        self.load_displacement_btn.setText("Load Displacement")
        self.load_displacement_btn.setStyleSheet("color: black; font-weight: regular;")

    def remove_all(self):
        self.remove_diffuse()
        self.remove_ao()
        self.remove_normal()
        self.remove_roughness()
        self.remove_metallic()
        self.remove_displacement()
        self.remove_opacity()

    def generate_albedo(self,base_path):
        if self.diffuse_img is not None:
            albedo = self.diffuse_img.copy()
        if self.ao_img is not None:
            if self.ao_img.shape != albedo.shape:
                self.ao_img = cv2.resize(self.ao_img, (albedo.shape[1], albedo.shape[0]))
            albedo = cv2.multiply(albedo.astype(np.float32) / 255.0,
                                  self.ao_img.astype(np.float32) / 255.0)
            albedo = (albedo * 255).astype(np.uint8)

        albedo = cv2.cvtColor(albedo, cv2.COLOR_BGR2RGB)

        # Add alpha from opacity if exists
        if self.opacity_img is not None:
            if self.opacity_img.shape[:2] != albedo.shape[:2]:
                self.opacity_img = cv2.resize(self.opacity_img, (albedo.shape[1], albedo.shape[0]))
            alpha = cv2.cvtColor(self.opacity_img, cv2.COLOR_BGR2GRAY)
        else:
            alpha = np.ones((albedo.shape[0], albedo.shape[1]), dtype=np.uint8) * 255

        albedo_rgba = cv2.merge((albedo, alpha))
        cv2.imwrite(base_path + "_albedo.tiff", albedo_rgba)
        print("Albedo saved.")

    def generate_specular(self, base_path):
        if self.diffuse_img is not None and self.metallic_img is not None:
            
            diffuse = self.diffuse_img.astype(np.float32) / 255.0
            metallic = self.metallic_img.astype(np.float32) / 255.0

            if len(metallic.shape) == 3:                
                metallic = cv2.cvtColor(metallic, cv2.COLOR_BGR2GRAY)

           
            dielectric_specular = np.full_like(diffuse, 0.04)           
            specular = dielectric_specular * (1.0 - metallic[..., np.newaxis]) + diffuse * metallic[..., np.newaxis]         
            specular = np.clip(specular * 255, 0, 255).astype(np.uint8)

            cv2.imwrite(base_path + "_spec.tiff", specular)
            print("Specular generation based on metallic.")
        else:
            print("Diffuse or Metallic not loaded.")


    def generate_normal(self,base_path):
        if self.normal_img is not None:
            normal = self.normal_img
            normal = cv2.cvtColor(normal, cv2.COLOR_BGR2RGB)
            if self.roughness_img is not None:                
                gloss = 1.0 - self.roughness_img.astype(np.float32) / 255.0
                gloss = np.clip(gloss * 255, 0, 255).astype(np.uint8)
                if len(gloss.shape) == 3:
                    gloss = cv2.cvtColor(gloss, cv2.COLOR_BGR2GRAY)
                if gloss.shape != normal.shape[:2]:
                    gloss = cv2.resize(gloss, (normal.shape[1], normal.shape[0]))
                ddna = cv2.merge((normal, gloss))
                cv2.imwrite(base_path + "_ddna.tiff", ddna)
                print("Normal + Gloss (_ddna) saved.")
            else:
                cv2.imwrite(base_path + "_ddn.tiff", normal)
                print("Normal (_ddn) saved.")

    def generate_displacement(self,base_path):
        if self.displacement_img is not None:
            cv2.imwrite(base_path + "_displ.tiff", self.displacement_img)
            print("Displacement saved.")

    def auto_load_from_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selectec Folder")
        if not folder:
            return

        suffix_map = {
            "_D": self.gen_albedo,
            "_AO": self.gen_ao,
            "_M": self.gen_metallic,
            "_R": self.gen_roughness,
            "_N": self.gen_normal,
            "_H": self.gen_displacement,
            "_O": self.gen_opacity,
            "_ORM": self.gen_orm,
        }

        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            name, ext = os.path.splitext(file)
            if ext.lower() not in [".png", ".jpg", ".jpeg", ".tiff", ".tga"]:
                continue

            for suffix, func in suffix_map.items():
                if name.endswith(suffix):
                    print(f"Loaded: {file} with: {func.__name__}")
                    func(full_path)
                    break

    def generate_output(self):       
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Textures", "", "")
        if not save_path:
            return

        
        base_path = os.path.splitext(save_path)[0]  # remove .png do final, se tiver

        self.generate_albedo(save_path)    
        self.generate_normal(save_path)    
        self.generate_specular(save_path)    
        self.generate_displacement(save_path)    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageLoaderApp()
    window.show()
    sys.exit(app.exec_())
