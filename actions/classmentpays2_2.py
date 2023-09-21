
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesclassementpays(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/classementpays.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllclassementpays()

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
    def refreshAllclassementpays(self):

        #self.refreshTable(self.ui.label_epreuves, self.ui.tableEpreuves, "SELECT numEp, nomEp, formeEp, nomDi, categorieEp, nbSportifsEp, dateEp FROM LesEpreuves")
        #self.refreshTable(self.ui.label_sportifs, self.ui.tableSportifs, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, numEq FROM LesSportifsEQ")
        self.refreshTable(self.ui.label_classmentpays, self.ui.tableclassmentpays, """ WITH PaysParticipants AS ( SELECT numPa, pays FROM LesParticpants JOIN LesSportifs_base ON (numPa=numEq or numPa=numSp)),
                                                                                                gold_pays AS(
                                                                                                    SELECT pays, COUNT(gold) AS nbGold
                                                                                                    FROM PaysParticipants LEFT JOIN LesResultats ON (numPa == gold)
                                                                                                    GROUP BY pays),
                                                                                                silver_pays AS(
                                                                                                    SELECT pays, COUNT(silver) AS nbSilver
                                                                                                    FROM PaysParticipants LEFT JOIN LesResultats ON (numPa == silver)
                                                                                                    GROUP BY pays),
                                                                                                bronze_pays AS(
                                                                                                    SELECT pays, COUNT(bronze) AS nbBronze
                                                                                                    FROM PaysParticipants LEFT JOIN LesResultats ON (numPa == bronze)
                                                                                                    GROUP BY pays)
                                                                                            SELECT A.pays, nbGold, nbSilver ,nbBronze FROM  gold_pays A 
                                                                                            JOIN silver_pays B  ON(A.pays=B.pays)
                                                                                            JOIN  bronze_pays C ON (B.pays=C.pays)
                                                                                            GROUP BY A.pays 
                                                                                            ORDER BY SUM( nbGold) DESC, SUM(nbSilver) DESC,SUM(nbBronze) DESC ; """)    
        #self.refreshTable(self.ui.label_agemoy, self.ui.tableagemoy, " with R1 as (SELECT gold from LesResultat join LesAgesSportifs on(gold.LesResultat=numSp.LesAgesSportifs)), R2 as (select count(gold) from R1)")