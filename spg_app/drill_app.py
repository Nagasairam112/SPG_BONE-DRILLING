from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
import os
import pandas as pd
from past.builtins import xrange
# from qtconsole.qt import QtCore, QtGui
import numpy as np
import qdarkstyle
import time
import subprocess
import shutil


qtcreator_file = "spg.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)
class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.file1.clicked.connect(self.selectFile)
        self.file2.clicked.connect(self.selectFile2)
        self.save.clicked.connect(self.selectDirectory)
        self.clean.clicked.connect(self.proce)
        self.merge.clicked.connect(self.mer)
        self.export_2.clicked.connect(self.expo)
        self.opna.clicked.connect(self.ops)
        self.mas.clicked.connect(self.mad)

        # Variables to store file paths
        self.tool1 = ""
        self.speci = ""
        self.out=     ""
        file_path_ready = pyqtSignal(str)


    def selectFile(self):
        # Open file dialog to select a file
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("LS-Dyna files (*.k)")

        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                file_path = file_paths[0]
                self.path1.setText(file_path)
                self.tool1=file_path
                # self.readFile(file_path)

    def selectFile2(self):
        # Open file dialog to select a file
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("LS-Dyna files (*.k)")

        if file_dialog.exec_():
            file_paths2 = file_dialog.selectedFiles()
            if file_paths2:
                file_path2 = file_paths2[0]
                self.path2.setText(file_path2)
                self.speci=file_path2

    def selectDirectory(self):
        # Open file dialog to select a directory
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')

        if directory:
            file_name = self.filena.text()
            if file_name:
                file_path = directory + '/' + file_name + '.k'
                try:
                    with open(file_path, 'w'):
                        print(f"File '{file_path}' created successfully!")
                        self.outpath.setText(file_path)  # Set file path to QLineEdit
                        self.out=file_path
                        msgBox = QMessageBox()
                        msgBox.setText(""+file_name+".k  is created")
                        msgBox.setWindowTitle("Message")
                        msgBox.setStandardButtons(QMessageBox.Ok)
                        msgBox.exec_()
                except Exception as e:
                    print(f"Failed to create file '{file_path}': {e}")
            else:
                print("Please enter a file name.")
        else:
            print("Please select a directory.")

    def getFilePath1(self):
        return self.tool1

    def getFilePath2(self):
        return self.speci

    def getFilePath3(self):
        return self.out

    def remove_lines_starting_with_dollar(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            if not (line.strip().startswith('$') and not line.strip().startswith('$#')):
                new_lines.append(line)

        with open(file_path, 'w') as file:
            file.writelines(new_lines)

    def write_to_file(self,file_path, include_file_path, include_auto_offset_file_path):
        try:
            content = f"""*KEYWORD
*INCLUDE
{include_file_path}
*INCLUDE_TRANSFORM
{include_auto_offset_file_path}
$#  idnoff    ideoff    idpoff    idmoff    idsoff    idfoff    iddoff
   1000001   1000001   1000001   1000001   1000001   1000001   1000001
$#  idroff         -    prefix    suffix
   1000001                              
$#  fctmas    fcttim    fctlen    fcttem   incout1    fctchg
       1.0       1.0       1.01.0                1       0.0
$#  tranid
         0
*END"""
            with open(file_path, 'w') as file:
                file.write(content)
            print("Content successfully written to the file.")
        except Exception as e:
            print("An error occurred:", e)

    def delete_lines_between_keywords(self,file1_path, wanted_keywords, unwanted_keywords):
        # Open the input file for reading
        with open(file1_path, 'r') as file:
            lines = file.readlines()

        # Flag to indicate whether to skip lines
        skip_lines = False

        # New lines list without the skipped lines
        new_lines = []

        # Iterate through each line
        for line in lines:
            # Check if any of the unwanted keywords are in the line
            if any(keyword in line for keyword in unwanted_keywords):
                # Set the flag to True to start skipping lines
                skip_lines = True
            # Check if any of the wanted keywords are in the line
            elif any(keyword in line for keyword in wanted_keywords):
                # Set the flag to False to stop skipping lines
                skip_lines = False
                # Append the line to the new lines list
                new_lines.append(line)
            # Check if the flag is False, meaning we're not skipping lines
            elif not skip_lines:
                # Append the line to the new lines list
                new_lines.append(line)

        # Write the new lines to the output file
        with open(file1_path, 'w') as file:
            file.writelines(new_lines)

    # def modify_section_solid_line(self,file_path):
    #     try:
    #         # Read the file
    #         with open(file_path, 'r') as file:
    #             lines = file.readlines()
    #
    #         # Find the line indices for lines between '*SECTION_SOLID' and the next '*'
    #         section_solid_index = None
    #         next_asterisk_index = None
    #         for i, line in enumerate(lines):
    #             if line.startswith('*SECTION_SOLID'):
    #                 section_solid_index = i
    #             elif section_solid_index is not None and line.startswith('*'):
    #                 next_asterisk_index = i
    #                 break
    #
    #         # Delete the lines between '*SECTION_SOLID' and the next '*'
    #         if section_solid_index is not None and next_asterisk_index is not None:
    #             del lines[section_solid_index + 1:next_asterisk_index]
    #
    #         # Find the index for the line under '*SECTION_SOLID'
    #         for i, line in enumerate(lines):
    #             if line.startswith('*SECTION_SOLID'):
    #                 section_solid_index = i + 1
    #                 break
    #
    #         # Insert '100,10,0' under the '*SECTION_SOLID' keyword
    #         if section_solid_index is not None:
    #             lines.insert(section_solid_index, "100,10,0\n")
    #
    #         # Write the modified content back to the same file
    #         with open(file_path, 'w') as file:
    #             file.writelines(lines)
    #
    #         print(
    #             "Lines between '*SECTION_SOLID' and the next '*' deleted, and '100,10,0' added under '*SECTION_SOLID' in the same file.")
    #
    #     except Exception as e:
    #         print("An error occurred:", e)
    #
    # def modify_mat_keyword(self,input_file_path):
    #     try:
    #         # Read the input file
    #         with open(input_file_path, 'r') as input_file:
    #             lines = input_file.readlines()
    #
    #         # Find the line indices for the '*MAT' keyword
    #         mat_indices = [i for i, line in enumerate(lines) if line.startswith('*MAT')]
    #
    #         # Iterate over each '*MAT' keyword
    #         for mat_index in mat_indices:
    #             second_line_index = mat_index + 2  # Second line under '*MAT'
    #             if second_line_index < len(lines):
    #                 parts = lines[second_line_index].split()
    #                 if len(parts) >= 2:
    #                     # Insert '100' as the first numeric value
    #                     parts[0] = '100'
    #                     # Join the parts with commas
    #                     modified_line = ','.join(parts)
    #                     lines[second_line_index] = modified_line + '\n'
    #
    #         # Create a temporary file path
    #         temp_file_path = input_file_path + '.tmp'
    #
    #         # Write the modified content to the temporary file
    #         with open(temp_file_path, 'w') as temp_file:
    #             temp_file.writelines(lines)
    #
    #         # Replace the original file with the temporary file
    #         shutil.move(temp_file_path, input_file_path)
    #
    #         print(
    #             "First numeric value set to '100' and commas added between values in the second line under '*MAT' keyword in the original file.")
    #
    #     except Exception as e:
    #         print("An error occurred:", e)
    #
    # def modify_part_keyword(self,file_path):
    #     try:
    #         # Read the file
    #         with open(file_path, 'r') as file:
    #             lines = file.readlines()
    #
    #         # Find the line indices for the '*PART' keyword (case-insensitive)
    #         part_indices = [i for i, line in enumerate(lines) if line.upper().startswith('*PART')]
    #
    #         # Iterate over each '*PART' keyword
    #         for part_index in part_indices:
    #             fourth_line_index = part_index + 3  # Fourth line under '*PART'
    #             if fourth_line_index < len(lines):
    #                 del lines[fourth_line_index]  # Delete the fourth line under '*PART'
    #                 break  # No need to iterate further if the line is deleted
    #
    #         # Insert the modified line under '*PART'
    #         for part_index in part_indices:
    #             modified_line = "1000,100,100,0,0,0,0,0\n"  # Modified line to be inserted
    #             lines.insert(part_index + 3, modified_line)
    #
    #             # Delete the line following the modified line
    #             del lines[part_index + 4]
    #
    #         # Write the modified content back to the file
    #         with open(file_path, 'w') as file:
    #             file.writelines(lines)
    #
    #         print("Fourth line under '*PART' keyword deleted and modifications added successfully in the same file.")
    #
    #     except Exception as e:
    #         print("An error occurred:", e)
    def add_section_above_end(self,file_path, section_lines):
        with open(file_path, "r") as file:
            lines = file.readlines()

        end_index = len(lines)  # Default to the end of the file
        for i, line in enumerate(lines):
            if line.strip().upper() == "END":
                end_index = i
                break

        lines = lines[:end_index] + section_lines + lines[end_index:]

        with open(file_path, "w") as file:
            file.writelines(lines)

    def remove_section(self,file_path, section_name):
        modified_lines = []
        removing = False

        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith(section_name):
                removing = True
            elif removing:
                if line.strip().startswith("*"):
                    removing = False
                    modified_lines.append(line)
                elif line.strip() == "":
                    pass  # Skip the empty line
                else:
                    continue  # Skip this line and continue removing
            else:
                modified_lines.append(line)

        with open(file_path, "w") as file:
            file.writelines(modified_lines)

    def open_program_with_file(self,program_path, file_path):
        try:
            # Open the program with the file
            subprocess.Popen([program_path, file_path])
            print("Program opened successfully with the file.")
        except FileNotFoundError:
            print("Error: Program not found at the specified path.")
        except Exception as e:
            print("An error occurred:", e)




    def mad(self):
        text = self.mats.toPlainText()



    def proce(self):
        try:
            a1= self.tool1
            print(a1)
            self.remove_lines_starting_with_dollar(a1)

        except Exception as e:
            print(e)

    def mer(self):
        try:
            a1= self.tool1
            a2= self.speci
            a3=self.out
            wanted_keywords = ['*SECTION_SOLID', '*part']
            unwanted_keywords = ['*DATABASE_FORMAT', '*CONTROL_TERMINATION', '*CONTROL_TIMESTEP', '*CONTROL_CONTACT',
                        '*CONTROL_ENERGY',
                        '*CONTROL_ACCURACY', '*CONTROL_BULK_VISCOSITY', '*CONTROL_SOLID', '*CONTROL_SHELL',
                        '*CONTROL_OUTPUT', '*CONTROL_PARALLEL',
                        '*CONTROL_SOLUTION', '*CONTROL_HOURGLASS', '*DATABASE_GLSTAT',
                        '*DATABASE_SPCFORC', '*DATABASE_RCFORC',
                        '*DATABASE_NCFORC', '*DATABASE_BNDOUT', '*DATABASE_NODOUT', '*DATABASE_MATSUM',
                        '*DATABASE_ELOUT', '*DATABASE_JNTFORC', '*DATABASE_DEFORC', '*DATABASE_EXTENT_BINARY',
                        '*DATABASE_BINARY_D3PLOT', '*DATABASE_BINARY_INTFOR', '*DATABASE_BINARY_D3PROP']
            section_lines = [
                "*SECTION_SOLID_SPG_TITLE\n",
                "Prop_SPG\n",
                "$#   secid    elform       aet    unused    unused    unused    cohoff   gaskeit\n",
                "         1        47         0                                     0.0       0.0\n",
                "$#      dx        dy        dz   ispline    kernel         -    smstep       msc\n",
                "       1.8       1.8       1.8         0         1                   5       0.0\n",
                "$#    idam        fs   stretch       itb     msfac       isc     boxid     pdamp\n",
                "         5      0.02       1.2         3       0.0       0.0         0    -0.001\n",
                "END\n"
            ]
            self.delete_lines_between_keywords(a1,wanted_keywords, unwanted_keywords)
            time.sleep(5)
            self.progrss.setValue(10)
            self.delete_lines_between_keywords(a2,wanted_keywords, unwanted_keywords)
            time.sleep(5)
            self.progrss.setValue(20)
            self.remove_section(a2,"*SECTION_SOLID")
            time.sleep(5)
            self.progrss.setValue(30)
            self.add_section_above_end(a2,section_lines)
            time.sleep(5)
            self.progrss.setValue(40)


        except Exception as e:
            print(e)

    def expo(self):
        a1 = self.tool1
        a2 = self.speci
        a3 = self.out
        self.write_to_file(a3,a2,a1)
        self.progrss.setValue(50)

    def ops(self):
        try:
           a1 = self.tool1
           a2 = self.speci
           a3 = self.out
           program_path = "C:\Program Files\LSTC\LS-PrePost 4.11\lsprepost4.11_x64.exe"
           self.open_program_with_file(program_path,a3 )
        except Exception as e:
            print(e)








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet()
    app.setStyleSheet(dark_stylesheet)
    app.setStyle('fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())