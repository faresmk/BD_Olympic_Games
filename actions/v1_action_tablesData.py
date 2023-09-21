
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesDataV1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_tablesData.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTablesV1()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)


    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAllTablesV1(self):

        #self.refreshTable(self.ui.label_epreuves, self.ui.tableEpreuves, "SELECT numEp, nomEp, formeEp, nomDi, categorieEp, nbSportifsEp, dateEp FROM LesEpreuves")
        #self.refreshTable(self.ui.label_sportifs, self.ui.tableSportifs, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, numEq FROM LesSportifsEQ")
        self.refreshTable(self.ui.label_LesDisciplines, self.ui.tableLesDisciplines, "SELECT nomDi FROM LesDisciplines")
        self.refreshTable(self.ui.label_LesParticpants, self.ui.tableLesParticpants, "SELECT numPa FROM LesParticpants")
        self.refreshTable(self.ui.label_LesSportifs_base, self.ui.tableLesSportifs_base, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, numEq FROM LesSportifs_base")
        self.refreshTable(self.ui.label_LesEquipes_base, self.ui.tableLesEquipes_base, "SELECT numEq FROM LesEquipes_base")
        self.refreshTable(self.ui.label_MembreEQ, self.ui.tableMembreEQ, "SELECT numEq, numSp FROM MembreEQ")    
        self.refreshTable(self.ui.label_LesEpreuves, self.ui.tableLesEpreuves, "SELECT numEp, nomEp, formeEp, nomDi, categorieEp, nbSportifsEp, dateEp FROM LesEpreuves")
        self.refreshTable(self.ui.label_LesResultats, self.ui.tableLesResultats, "SELECT numEp, gold, silver, bronze FROM LesResultats")
        self.refreshTable(self.ui.label_LesInscriptions, self.ui.tableLesInscriptions, "SELECT numIn, numEp FROM LesInscriptions")
    

        # TODO 1.3 : modifier pour afficher les nouveaux éléments (il faut aussi changer le fichier .ui correspondant)
        # TODO 1.4b : ajouter l'affichage des éléments de la vue LesAgesSportifs après l'avoir créée
        self.refreshTable(self.ui.label_LesAgesSportifs, self.ui.tableLesAgesSportifs, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, Age, numEq FROM LesAgesSportifs")
        # TODO 1.5b : ajouter l'affichage des éléments de la vue LesNbsEquipiers après l'avoir créée
        self.refreshTable(self.ui.label_LesNbsEquipiers, self.ui.tableLesNbsEquipiers, "SELECT numEq, NbsEquipiers FROM LesNbsEquipiers")