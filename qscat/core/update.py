# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import os
import packaging.version
import requests
import shutil
import sys
import zipfile

from qgis.core import Qgis
from qgis.core import QgsApplication
from qgis.core import QgsMessageLog
from qgis.core import QgsSettings
from qgis.core import QgsTask

from qgis.utils import iface
from qgis.utils import reloadPlugin

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl

from PyQt5.QtGui import QDesktopServices

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout

from qscat.core.utils import datetime_now
from qscat.core.utils import get_metadata_version
# from qscat.core.utils import get_plugin_dir
# from qscat.core.utils import get_plugins_dir

#from qgis.utils import reloadPlugin

LOCAL_PLUGIN_NAME = 'qscat'
REPOSITORY_NAME = 'qscat'
REPOSITORY_USERNAME = 'louisfacun'


def check_updates_on_click(self):
    globals()['check_updates_on_click'] = CheckUpdatesTask()
    QgsApplication.taskManager().addTask(globals()['check_updates_on_click'])

    globals()['check_updates_on_click'].taskCompleted.connect(
        lambda: check_updates_on_click_task_complete(self)
    )


def check_updates_on_click_task_complete(self):
    task = globals()['check_updates_on_click']
    if task.status() == QgsTask.Complete:
        release_info = task.release_info

        latest_version = release_info['tag_name']
        release_zip_url = release_info['zipball_url']
        
        s = QgsSettings()
        s.setValue("qscat/latest_version", latest_version)

        # Parse the current version from the metadata.txt file
        current_version = get_metadata_version()

        last_checked_datetime = datetime_now()
        self.dockwidget.lbl_about_latest_version.setText(
            f'You have the latest version ({latest_version}) '\
            f'(last checked {last_checked_datetime})'
        )
        # Compare the versions and update if necessary
        if is_newer_version(latest_version, current_version):
            release_note = release_info['body']
            show_update_details_dialog(
                current_version, 
                latest_version,
                release_note,
                release_zip_url,
            )
        else:
            show_no_update_dialog()

        s.setValue("qscat/last_checked_datetime", last_checked_datetime)


def check_updates_on_start():
    globals()['check_updates_on_start'] = CheckUpdatesTask()
    QgsApplication.taskManager().addTask(globals()['check_updates_on_start'])

    globals()['check_updates_on_start'].taskCompleted.connect(
        check_updates_on_start_task_complete
    )


def check_updates_on_start_task_complete():
    task = globals()['check_updates_on_start']
    if task.status() == QgsTask.Complete:
        release_info = task.release_info

        # For on start update, we only care about success status
        if release_info['status'] == 'SUCCESS':
            latest_version = release_info['tag_name']
            release_zip_url = release_info['zipball_url']
            release_note = release_info['body']

            s = QgsSettings()
            s.setValue("qscat/latest_version", latest_version)

            # Parse the current version from the metadata.txt file
            current_version = get_metadata_version()
            if is_newer_version(latest_version, current_version):
                widget = iface.messageBar().createMessage(
                    'Notice',
                    f'A new version qscat-{latest_version} is available!'
                )
                button = QPushButton(widget)
                button.setText("View details")
                button.pressed.connect(lambda: show_update_details_dialog(
                    current_version, 
                    latest_version,
                    release_note,
                    release_zip_url,
                ))
                widget.layout().addWidget(button)
                iface.messageBar().pushWidget(widget, Qgis.Info)


def open_latest_release_url():
    url = QUrl(f"https://github.com/{REPOSITORY_USERNAME}/{REPOSITORY_NAME}/releases/latest")
    QDesktopServices.openUrl(url)


# def update_plugin(release_zip_url):
#     """Apply downloads and installation (copy and paste)."""
#     globals()['update_plugin'] = UpdatePluginTask(release_zip_url)
#     QgsApplication.taskManager().addTask(globals()['update_plugin'])

#     globals()['update_plugin'].taskCompleted.connect(
#         update_plugin_task_complete
#     )


# def update_plugin_task_complete():
#     task = globals()['update_plugin']
#     if task.status() == QgsTask.Complete:
#         for key in [key for key in sys.modules.keys()]:
#             if '{}.'.format(LOCAL_PLUGIN_NAME) in key:
#                 if hasattr(sys.modules[key], 'qCleanupResources'):
#                     sys.modules[key].qCleanupResources()
#                 del sys.modules[key]

#         iface.messageBar().clearWidgets()
#         reloadPlugin(LOCAL_PLUGIN_NAME)
#         show_update_complete_dialog()


class CheckUpdatesTask(QgsTask):
    def __init__(self):
        super().__init__("Checking updates", QgsTask.CanCancel)
        self.release_info = None
        self.exception = None

    def run(self):
        QgsMessageLog.logMessage(
            message=f"Started task: <b>{self.description()}</b>.",
            level=Qgis.Info,
        )
        try:
            self.release_info = check_updates()
            return True
        
        except Exception as e:
            self.exception = e
            return False

    def finished(self, result):
        if self.isCanceled():
            QgsMessageLog.logMessage(
                message=f"Canceled task: <b>{self.description()}</b>.",
                level=Qgis.Warning,
            )
            return
        elif not result:
            QMessageBox.critical(
                iface.mainWindow(),
                f"Task error: : <b>{self.description()}</b>.",
                f"The following error occurred:" \
                f"\n{self.exception.__class__.__name__}: {self.exception}",
            )
            return
        QgsMessageLog.logMessage(
            message=f"Success task: <b>{self.description()}</b>",
            level=Qgis.Success,
        )


# class UpdatePluginTask(QgsTask):
#     def __init__(self, release_zip_url):
#         super().__init__("Updating plugin", QgsTask.CanCancel)
#         self.release_zip_url = release_zip_url
#         self.exception = None

#     def run(self):
#         QgsMessageLog.logMessage(
#             message=f"Started task: <b>{self.description()}</b>.",
#             level=Qgis.Info,
#         )
#         try:
#             release_zip = download_plugin(self.release_zip_url)
#             # Update the plugin by deleting the old files and copying the new files
#             install_plugin(release_zip)

#             return True
        
#         except Exception as e:
#             self.exception = e
#             return False

#     def finished(self, result):
#         if self.isCanceled():
#             QgsMessageLog.logMessage(
#                 message=f"Canceled task: <b>{self.description()}</b>.",
#                 level=Qgis.Warning,
#             )
#             return
#         elif not result:
#             QMessageBox.critical(
#                 iface.mainWindow(),
#                 f"Task error: : <b>{self.description()}</b>.",
#                 f"The following error occurred:"\
#                 f"\n{self.exception.__class__.__name__}: {self.exception}",
#             )
#             return
        
#         QgsMessageLog.logMessage(
#             message=f"Success task: <b>{self.description()}</b>",
#             level=Qgis.Success,
#         )


# def install_plugin(release_zip):
#     """Extract, copy and paste latest release zip to plugin directory."""
#     plugin_dir = get_plugin_dir()
#     plugins_dir = get_plugins_dir()

#     # Define temp folder where to copy the contents of the zip file
#     temp_dir = os.path.join(plugins_dir, 'temp')

#     # Delete temp folder if exists
#     if os.path.exists(temp_dir):
#         shutil.rmtree(temp_dir)

#     # Extract the zip file
#     with zipfile.ZipFile(release_zip, 'r') as zip_ref:
#         zip_ref.extractall(temp_dir)

#     # Get the username-repo-commit_id folder > qscat
#     for directory in os.listdir(temp_dir):
#         if directory.startswith(f'{REPOSITORY_USERNAME}-'):
#             source_dir = os.path.join(temp_dir, directory, REPOSITORY_NAME)
#             break

#     shutil.copytree(source_dir, plugin_dir, dirs_exist_ok=True)

#     # Remove download zip and temp dir
#     os.remove(release_zip)
#     shutil.rmtree(temp_dir)


# def download_plugin(release_zip_url):
#     plugin_dir = get_plugin_dir()

#     # Download the zip file using request
#     response = requests.get(release_zip_url, headers=headers)

#     # Define where to save the release zip
#     release_zip = os.path.join(plugin_dir, 'release.zip')
    
#     # Save the zip file from response
#     with open(release_zip, 'wb') as f:
#         f.write(response.content)

#     return release_zip


def check_updates():
    release_info = get_latest_release_info(
        REPOSITORY_USERNAME ,
        REPOSITORY_NAME,
    )
    return release_info


def get_latest_release_info(username, repository):
    """Get latest release info from the GitHub repository.
    
    Args:
        username (str): GitHub username (louisfacun)
        repository (str): GitHub repository (qscat)

    Returns:
        dict: tag_name, body, zipball_url
    """
    api_url = f'https://api.github.com/repos/{username}/{repository}/releases/latest'
    #headers = {"Authorization": f"token {access_token}"}

    try:
        response = requests.get(api_url, timeout=50)
        response_json = response.json()
        return {
            'status': 'SUCCESS',
            'tag_name': response_json['tag_name'],
            'body': response_json['body'],
            'zipball_url': response_json['zipball_url'],
        }
    except requests.exceptions.Timeout:
        return {'status': 'TIMEOUT'}
    except requests.exceptions.TooManyRedirects:
        return {'status': 'BAD_URL'}
    except requests.exceptions.RequestException as e:
        return {'status': 'UNKNOWN_ERROR'}


def is_newer_version(tag_name, version):
    """Check if GitHub repo latest release tag (version) is newer than the
    local QGIS plugin metadata.txt version.

    Args:
        tag_name (str): The version 'tag' from GitHub repo. Eg. v1.0.0-beta
        version (str): The version from QGIS plugin metadata.txt Eg. 1.0.0-beta

    Returns:
        boolean
    """
    latest_version = packaging.version.parse(tag_name.lstrip('v'))
    current_version = packaging.version.parse(version)
    return latest_version > current_version


# Dialogs
def show_no_update_dialog():
    msg_box = QMessageBox()
    msg_box.setText("There are currently no updates available.")
    msg_box.setWindowTitle("QSCAT")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.exec_()

"""
def show_update_complete_dialog():
    msg_box = QMessageBox()
    msg_box.setText("Updates are complete. Please restart QGIS.")
    msg_box.setWindowTitle("QSCAT")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.exec_()


def show_update_confirmation_dialog(dialog, release_zip_url):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Warning. Please Read!")
    msg_box.setText("Please do not interrupt the update process. " \
                    "Interrupting the update process may result in " \
                    "incomplete installation or errors. Also, before " \
                    "proceeding with the update, please note that it is "\
                    "recommended to restart QGIS once the update is complete. "\
                    "So, please ensure that you have saved any unfinished work "\
                    "before starting the update process. Continue?")
    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg_box.setDefaultButton(QMessageBox.Cancel)
    msg_box.setIcon(QMessageBox.Warning)
    result = msg_box.exec_()
    if result == QMessageBox.Ok:
        update_plugin(release_zip_url)
        dialog.close()
"""

def show_update_details_dialog(
    current_version,
    latest_version,
    release_note,
    release_zip_url
 ):
    # Let's just remove symbols from this markdown
    release_note = release_note.replace('#', '')
    release_note = release_note.replace('`', '')

    dialog = QDialog()
    dialog.setWindowTitle("QSCAT - Update is available!")

    update_note = f'Your current version: v{current_version}.\n' \
                  f'Latest version available: {latest_version}.\n\n{release_note}'
    text_browser = QTextBrowser()
    text_browser.setPlainText(update_note)
    text_browser.setOpenExternalLinks(True)
    text_browser.setTextInteractionFlags(
        text_browser.textInteractionFlags() 
        | Qt.LinksAccessibleByMouse 
        | Qt.LinksAccessibleByKeyboard
    )

    update_button = QPushButton("Update (open url)")
    # Temporary disable download-update function, open url instead
    """
    update_button.clicked.connect(lambda: show_update_confirmation_dialog(
        dialog,
        release_zip_url
    ))
    """
    update_button.clicked.connect(open_latest_release_url)

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(dialog.close)

    buttons_widget = QWidget()
    hboxlayout = QHBoxLayout()
    hboxlayout.addWidget(update_button)
    hboxlayout.addWidget(cancel_button)
    buttons_widget.setLayout(hboxlayout)

    layout = QVBoxLayout()
    layout.addWidget(text_browser)
    layout.addWidget(buttons_widget)

    dialog.setLayout(layout)
    dialog.setFixedWidth(500)
    dialog.exec_()