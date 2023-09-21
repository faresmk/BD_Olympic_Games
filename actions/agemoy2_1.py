
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesAgeMoy(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/agemoy.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTablesAgeMoy()

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
    def refreshAllTablesAgeMoy(self):

        #self.refreshTable(self.ui.label_epreuves, self.ui.tableEpreuves, "SELECT numEp, nomEp, formeEp, nomDi, categorieEp, nbSportifsEp, dateEp FROM LesEpreuves")
        #self.refreshTable(self.ui.label_sportifs, self.ui.tableSportifs, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, numEq FROM LesSportifsEQ")
        self.refreshTable(self.ui.label_agemoy, self.ui.tableagemoy, """With R2 as (SELECT DISTINCT numEq, numSp from LesResultats join MembreEQ on(gold=numEq))
                                                                        SELECT avg(Age) AS moyAge FROM LesAgesSportifs R1 join R2 on (R1.numSp = R2.numSp);""")    
        #self.refreshTable(self.ui.label_agemoy, self.ui.tableagemoy, " with R1 as (SELECT gold from LesResultat join LesAgesSportifs on(gold.LesResultat=numSp.LesAgesSportifs)), R2 as (select count(gold) from R1)")