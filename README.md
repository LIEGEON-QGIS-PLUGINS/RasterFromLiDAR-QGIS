# Raster from LiDAR

<table>
<tr>
<td><img src="icon.png" alt="Logo du plugin" width="400"/></td>
<td>
<p>Le plugin <strong>Raster from LiDAR</strong> permet de générer automatiquement des <strong>MNT (Modèles Numériques de Terrain)</strong> et des <strong>ombrages</strong> à partir de fichiers LiDAR classifiés (.las ou .laz). L’utilisateur peut <strong>sélectionner les classes de points à conserver</strong> (par ex. sol, végétation basse, etc.) afin de personnaliser le MNT produit. Il offre également la possibilité de <strong>remplir les valeurs nulles</strong> sur le MNT.</p>
</td>
</tr>
</table>

---

## Compatibilité

- **QGIS 3.32** (testé uniquement sur cette version).
Il est possible que le plugin fonctionne avec d’autres versions de QGIS, mais cela n’a pas été testé.

>⚠️ Aucune nouvelle version n’est prévue. 

- **Dépendances (incluses nativement avec QGIS) :**
  - PyQt5
  - QGIS Processing Toolbox
  - GDAL

> ⚠️ Aucune installation externe n’est nécessaire.

---

## Installation

1. Téléchargez la dernière version dans [Releases](https://github.com/LIEGEON-QGIS-PLUGINS/RasterFromLiDAR-QGIS/releases) (ZIP).  
2. Dans QGIS, allez dans `Extensions > Installer une extension depuis un fichier ZIP`.  
3. Sélectionnez le fichier ZIP téléchargé et installez-le.  
4. Redémarrez QGIS si nécessaire.  

---

## Utilisation

1. Ouvrez le plugin via le menu `LiDAR Tools > Raster from LiDAR`.  
2. Sélectionnez le **dossier contenant les fichiers LiDAR**.  
3. Définissez les dossiers de sortie pour le MNT et l’ombrage.
4. Configurez les paramètres liés aux classes de points.  
5. Optionnel : activez le remplissage des valeurs nulles et configurez les paramètres de tuiles.  
6. Cliquez sur **Lancer le traitement**.  

> ⚠️ **Attention :** le traitement peut prendre beaucoup de temps selon la taille et le nombre de fichiers LiDAR.

---

## Données de test

Vous pouvez tester le plugin avec des fichiers LiDAR exemple disponibles ici : [Lien vers données test du LiDAR HD de l'IGN](https://geoservices.ign.fr/lidarhd)

---

## Licence

Ce plugin est fourni **“tel quel”**, sans garantie d’aucune sorte.  
Licence : MIT / Open-source.

---

## Renonciation

L’auteur **ne peut être tenu responsable** des dommages éventuels liés à l’utilisation du plugin ou aux données traitées.
