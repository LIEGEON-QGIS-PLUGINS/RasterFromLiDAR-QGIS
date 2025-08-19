import os
from qgis.core import QgsProject, QgsRasterLayer
import processing
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QWidget, QAction
from PyQt5.QtGui import QIcon

# -------------------------------
# Classe UI pour le plugin
# -------------------------------
class RasterFromLiDARUI(QWidget):
    def __init__(self):
        super().__init__()

        # Chemin complet vers le fichier .ui dans le même dossier que ce script
        ui_path = os.path.join(os.path.dirname(__file__), "RasterFromLiDAR.ui")
        uic.loadUi(ui_path, self)

        # Connecter boutons parcourir
        self.pushButton_input.clicked.connect(lambda: self.browse_folder(self.lineEdit_input))
        self.pushButton_output_mnt.clicked.connect(lambda: self.browse_folder(self.lineEdit_output_mnt))
        self.pushButton_output_hillshade.clicked.connect(lambda: self.browse_folder(self.lineEdit_output_ombrage))

        # Activer/désactiver champs distance/itérations selon checkbox
        self.checkBox_fillnodata.stateChanged.connect(self.toggle_fill_params)
        self.toggle_fill_params()  # initial

        # Bouton lancer traitement
        self.pushButton_run.clicked.connect(self.run_processing)

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if folder:
            line_edit.setText(folder)

    def toggle_fill_params(self):
        enabled = self.checkBox_fillnodata.isChecked()
        self.spinBox_distance.setEnabled(enabled)
        self.spinBox_iterations.setEnabled(enabled)

    def run_processing(self):
        dossier_entree = self.lineEdit_input.text()
        dossier_sortie_mnt = self.lineEdit_output_mnt.text()
        dossier_sortie_ombrage = self.lineEdit_output_ombrage.text()

        remplir_valeurs_nulles = self.checkBox_fillnodata.isChecked()
        distance_remplissage = self.spinBox_distance.value()
        iterations_remplissage = self.spinBox_iterations.value()

        champ_classification = self.lineEdit_champ_class.text()
        valeurs_classification = [int(v.strip()) for v in self.lineEdit_valeurs_class.text().split(',') if v.strip()]

        resolution_raster = self.doubleSpinBox_resolution.value()
        taille_tuile = self.spinBox_tile.value()

        azimut_soleil = self.spinBox_azimuth.value()
        angle_soleil = self.spinBox_angle.value()
        facteur_z = self.doubleSpinBox_zfactor.value()

        # Création des dossiers de sortie si nécessaire
        os.makedirs(dossier_sortie_mnt, exist_ok=True)
        os.makedirs(dossier_sortie_ombrage, exist_ok=True)

        # Lister les fichiers LiDAR
        fichiers_lidar = [f for f in os.listdir(dossier_entree) if f.lower().endswith(('.las', '.laz'))]

        for fichier in fichiers_lidar:
            chemin_entree = os.path.join(dossier_entree, fichier)
            nom_base = os.path.splitext(fichier)[0]

            # --- Export MNT ---
            sortie_mnt = os.path.join(dossier_sortie_mnt, f'{nom_base}_MNT.tif')
            params_raster = {
                'INPUT': chemin_entree,
                'ATTRIBUTE': 'Z',
                'FILTER_EXPRESSION': f"{champ_classification} IN ({','.join(map(str, valeurs_classification))})",
                'RESOLUTION': resolution_raster,
                'TILE_SIZE': taille_tuile,
                'OUTPUT': sortie_mnt
            }
            processing.run('pdal:exportraster', params_raster)
            layer_mnt = QgsRasterLayer(sortie_mnt, f'{nom_base}_MNT')
            if layer_mnt.isValid(): 
                QgsProject.instance().addMapLayer(layer_mnt)
            mnt_a_utiliser = sortie_mnt

            # --- Remplir valeurs nulles ---
            if remplir_valeurs_nulles:
                sortie_mnt_filled = os.path.join(dossier_sortie_mnt, f'{nom_base}_MNT_interpoler.tif')
                params_fill = {
                    'INPUT': mnt_a_utiliser,
                    'BAND': 1,
                    'DISTANCE': distance_remplissage,
                    'ITERATIONS': iterations_remplissage,
                    'MASK_LAYER': None,
                    'NO_MASK': False,
                    'OPTIONS': '',
                    'OUTPUT': sortie_mnt_filled
                }
                processing.run('gdal:fillnodata', params_fill)
                mnt_a_utiliser = sortie_mnt_filled
                layer_mnt_filled = QgsRasterLayer(sortie_mnt_filled, f'{nom_base}_MNT_filled')
                if layer_mnt_filled.isValid():
                    QgsProject.instance().addMapLayer(layer_mnt_filled)

            # --- Ombrage ---
            sortie_ombrage = os.path.join(dossier_sortie_ombrage, f'{nom_base}_Ombrage.tif')
            params_hillshade = {
                'INPUT': mnt_a_utiliser,
                'AZIMUTH': azimut_soleil,
                'V_ANGLE': angle_soleil,
                'Z_FACTOR': facteur_z,
                'OUTPUT': sortie_ombrage
            }
            processing.run('native:hillshade', params_hillshade)
            layer_ombrage = QgsRasterLayer(sortie_ombrage, f'{nom_base}_Ombrage')
            if layer_ombrage.isValid():
                QgsProject.instance().addMapLayer(layer_ombrage)

        print("Traitement terminé")

# -------------------------------
# Classe Plugin QGIS
# -------------------------------
class LiDARPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.window = None
        self.action = None

    def initGui(self):
        # Chemin vers l'icône
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

        self.action = QAction(icon, "Raster from LiDAR", self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        # Ajouter au menu et à la barre d'outils
        self.iface.addPluginToMenu("&LiDAR Tools", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        # Retirer du menu et de la barre d'outils
        if self.action:
            self.iface.removePluginMenu("&LiDAR Tools", self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action = None

    def run(self):
        if self.window is None:
            self.window = RasterFromLiDARUI()
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

# -------------------------------
# Fonction de QGIS pour charger le plugin
# -------------------------------
def classFactory(iface):
    return LiDARPlugin(iface)
