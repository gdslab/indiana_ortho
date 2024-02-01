# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IndianaOrtho
                                 A QGIS plugin
 This plugin provide easy access to Indiana Ortho Imageries
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-04-07
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Jinha Jung
        email                : jinha@purdue.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsRasterLayer, QgsProject

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .indiana_ortho_dialog import IndianaOrthoDialog
import os.path


class IndianaOrtho:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "IndianaOrtho_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&Indiana Ortho Imagery")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        self.county_names = [
            "adams",
            "benton",
            "blackford",
            "clark",
            "daviess",
            "dearborn",
            "decatur",
            "dekalb",
            "delaware",
            "dubois",
            "dnr",
            "fayette",
            "floyd",
            "franklin",
            "gibson",
            "grant",
            "hancock",
            "henry",
            "huntingburg_city",
            "huntington",
            "huntington_city",
            "indnr",
            "jasper",
            "jay",
            "jefferson",
            "jennings",
            "knox",
            "lake",
            "lagrange",
            "laporte",
            "madison",
            "madison_hanover",
            "martin",
            "newton",
            "noble",
            "ohio",
            "perry",
            "pike",
            "porter",
            "posey",
            "randolph",
            "ripley",
            "rush",
            "scott",
            "shelby",
            "shelbyville",
            "spencer",
            "steuben",
            "switzerland",
            "tippecanoe",
            "union",
            "vanderburgh",
            "vermillion",
            "warrick",
            "wayne",
            "wells",
            "white",
            "whitley",
            "allen",
            "bartholomew",
            "boone",
            "brown",
            "carroll",
            "cass",
            "clinton",
            "crawford",
            "elkhart",
            "fulton",
            "hamilton",
            "harrison",
            "hendricks",
            "howard",
            "jackson",
            "johnson",
            "kosciusko",
            "lawrence",
            "marion",
            "marshall",
            "miami",
            "monroe",
            "morgan",
            "orange",
            "pulaski",
            "starke",
            "stjoseph",
            "tipton",
            "wabash",
            "washington",
            "clay",
            "fountain",
            "greene",
            "montgomery",
            "owen",
            "parke",
            "putnam",
            "sullivan",
            "vigo",
            "warren",
        ]

        self.county_names.sort()

        self.ortho_years = {
            "adams": ["2022", "2017"],
            "blackford": ["2022", "2017"],
            "clark": ["2022", "2017"],
            "daviess": ["2023", "2019"],
            "dearborn": ["2022", "2017"],
            "decatur": ["2022", "2017"],
            "dekalb": ["2022", "2017"],
            "delaware": ["2022", "2017"],
            "dubois": ["2023", "2019"],
            "fayette": ["2022", "2017"],
            "floyd": ["2022", "2017"],
            "franklin": ["2022", "2017"],
            "gibson": ["2023", "2017"],
            "grant": ["2022", "2017"],
            "hancock": ["2022", "2017"],
            "henry": ["2022", "2017"],
            "huntingburg_city": ["2023", "2018"],
            "huntington": ["2022", "2017"],
            "huntington_city": ["2022"],
            "indnr": ["2022", "2021"],
            "jay": ["2022", "2017"],
            "jefferson": ["2022", "2017"],
            "jennings": ["2022", "2017"],
            "knox": ["2023", "2019"],
            "lagrange": ["2022", "2017"],
            "madison": ["2022", "2017"],
            "madison_hanover": ["2022"],
            "martin": ["2023", "2019"],
            "noble": ["2022", "2017"],
            "ohio": ["2022", "2017"],
            "perry": ["2023", "2019"],
            "pike": ["2023", "2019"],
            "posey": ["2023", "2019"],
            "randolph": ["2022", "2017"],
            "ripley": ["2022", "2017"],
            "rush": ["2022", "2017"],
            "scott": ["2022", "2017"],
            "shelby": ["2022", "2017"],
            "shelbyville": ["2022", "2017"],
            "spencer": ["2023", "2019"],
            "steuben": ["2022", "2017"],
            "switzerland": ["2022", "2017"],
            "union": ["2022", "2017"],
            "vanderburgh": ["2023", "2019"],
            "vermillion": ["2023", "2019"],
            "warrick": ["2023", "2019"],
            "wayne": ["2022", "2017"],
            "wells": ["2022", "2017"],
            "whitley": ["2022", "2017"],
            "allen": ["2021", "2018"],
            "bartholomew": ["2021"],
            "boone": ["2021"],
            "brown": ["2021"],
            "carroll": ["2021"],
            "cass": ["2021"],
            "clinton": ["2021"],
            "crawford": ["2021", "2017"],
            "elkhart": ["2021"],
            "fulton": ["2021"],
            "hamilton": ["2023", "2021", "2017"],
            "harrison": ["2021"],
            "hendricks": ["2021"],
            "howard": ["2021"],
            "jackson": ["2021"],
            "johnson": ["2021"],
            "kosciusko": ["2021"],
            "lawrence": ["2021", "2017"],
            "marion": ["2021"],
            "marshall": ["2021"],
            "miami": ["2021", "2017"],
            "monroe": ["2021", "2019"],
            "morgan": ["2021"],
            "orange": ["2021", "2017"],
            "pulaski": ["2021"],
            "starke": ["2021"],
            "stjoseph": ["2021"],
            "tipton": ["2021"],
            "wabash": ["2021"],
            "washington": ["2021", "2017"],
            "clay": ["2023", "2018"],
            "fountain": ["2023", "2018"],
            "greene": ["2023", "2018"],
            "montgomery": ["2023", "2018"],
            "owen": ["2023", "2018"],
            "parke": ["2023", "2018"],
            "putnam": ["2023", "2018"],
            "sullivan": ["2023", "2018"],
            "vigo": ["2023", "2018"],
            "warren": ["2023", "2018"],
            "benton": ["2023", "2018"],
            "jasper": ["2023", "2018"],
            "lake": ["2023", "2018"],
            "laporte": ["2023", "2018"],
            "newton": ["2023", "2018"],
            "porter": ["2023", "2018"],
            "tippecanoe": ["2023", "2018"],
            "white": ["2023", "2018"],
            "dnr": ["2023"],
        }

        self.quality = ["high", "medium", "low"]

        self.ortho_base_dir = "https://lidar.digitalforestry.org/state/"

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("IndianaOrtho", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ":/plugins/indiana_ortho/icon.png"
        self.add_action(
            icon_path,
            text=self.tr("Indiana Ortho Imagery"),
            callback=self.run,
            parent=self.iface.mainWindow(),
        )

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr("&Indiana Ortho Imagery"), action)
            self.iface.removeToolBarIcon(action)

    def generate_cog_url(self):
        selected_county = self.dlg.comboBox_county.currentText()
        selected_year = self.dlg.comboBox_year.currentText()
        selected_quality = self.dlg.comboBox_quality.currentText()

        if selected_quality == "high":
            cog_url = (
                self.ortho_base_dir
                + f"{selected_year}/{selected_county}/{selected_county}_{selected_year}_ortho.tif"
            )
        elif selected_quality == "medium":
            cog_url = (
                self.ortho_base_dir
                + f"{selected_year}/{selected_county}/{selected_county}_{selected_year}_ortho_c.tif"
            )
        else:
            cog_url = (
                self.ortho_base_dir
                + f"{selected_year}/{selected_county}/{selected_county}_{selected_year}_ortho_cc.tif"
            )

        self.dlg.textEdit_cog_url.setText(cog_url)

    def add_to_map(self):
        cog_url = self.dlg.textEdit_cog_url.toPlainText()
        selected_county = self.dlg.comboBox_county.currentText()
        selected_year = self.dlg.comboBox_year.currentText()
        # print(f"Indiana_{selected_county}_{selected_year}_ortho")
        rlayer = QgsRasterLayer(
            "/vsicurl/" + cog_url, f"Indiana_{selected_county}_{selected_year}_ortho"
        )
        if rlayer.isValid():
            QgsProject().instance().addMapLayer(rlayer)
        else:
            print("Not valid.")

        # Make value of 0 as transparent
        layer = self.iface.activeLayer()
        provider = layer.dataProvider()
        provider.setNoDataValue(1, 0)

        # Now zoom to the added layer
        self.iface.zoomToActiveLayer()
        self.iface.mapCanvas().refresh()

    def update_year(self):
        self.dlg.comboBox_year.clear()
        selected_county = self.dlg.comboBox_county.currentText()
        self.dlg.comboBox_year.addItems(self.ortho_years[selected_county])

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = IndianaOrthoDialog()
            # Initialize combo boxes
            self.dlg.comboBox_county.clear()
            self.dlg.comboBox_year.clear()
            self.dlg.comboBox_quality.clear()
            self.dlg.comboBox_county.addItems(self.county_names)
            self.dlg.comboBox_quality.addItems(self.quality)
            selected_county = self.dlg.comboBox_county.currentText()
            self.dlg.comboBox_year.addItems(self.ortho_years[selected_county])
            # Event handlers
            self.dlg.pushButton_add.clicked.connect(self.add_to_map)
            self.dlg.comboBox_county.currentIndexChanged.connect(self.generate_cog_url)
            self.dlg.comboBox_county.currentIndexChanged.connect(self.update_year)
            self.dlg.comboBox_quality.currentIndexChanged.connect(self.generate_cog_url)
            self.dlg.comboBox_year.currentIndexChanged.connect(self.generate_cog_url)
            self.generate_cog_url()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
