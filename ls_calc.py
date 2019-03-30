# sl_calc.py   Author: Akira Hakuta, Date: 2019/03/31
# pythonw.exe ls_calc.py
# LaTeX SymPy Calculator is a calculator with LaTeX expression Form by using SymPy.
import sys
import os
#from PySide import QtCore,QtGui
from PyQt4 import QtCore,QtGui

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm' # to revert to old style (matplotlib 1.5)
matplotlib.rcParams['mathtext.rm'] = 'serif' # to revert to old style (matplotlib 1.5)


from sympy import *
F=Function('F')
f=Function('f')
var('a:z') 
var('A:DF:HJ:MP:RT:Z')

# variable : a,b,...,z,A,B,..,Z,\\alpha, \\beta,..,\pi,...,\\omega (except E, I, N, O, S, zeta, omicron)
# math constant : pi --> \\ppi, imaginary unit --> \\ii, napier constant --> \\ee
# LaTeX Code Style : \\sin{x},  \\log_{2}{8}, \\sum_{k=1}^{n}{k(k+1)^2}, ...

from antlr4_tex2sym import tex2sym, mylatex, mylatexstyle

import re


SLC_TITLE="LaTeX SymPy Calculator Ver. 1.2"

MAINFRAME_WIDTH=1600
MAINFRAME_HIGHT=900
CALCULATION_LIST_WIDTH=300

CALCULATION_LIST=['simplify','expand','factor','convert-to-decimal','nsimplify','complete-square-x', 
    'equation-x','equation-xy', 'equation-xyz','inequality-x-1','inequality-x-2', 'simplify-power', 'expand-log', 'expand-trig',
    'rationalize-denom','sqrtdenest', 'recursive-form-1', 'recursive-form-2','diff-equation-f(x)'
    ]
calculation_dict ={}
index =0
for el in CALCULATION_LIST:
    calculation_dict.update({el:index})
    index += 1

math_form_list = [['\\times ', '','\u00D7'],['\\cdot ', '','\u2219'],['\\div ', '','\u00F7'],['^{}', '','^'],['_{}','','_'],
            ['\\leqq ', '','\u2266'],['\\geqq ', '','\u2267'],
            ['\\ppi ', '','\u03C0'],['\\ii ','',"i"],['\\ee ','','e'],
            ['\\frac{}{}','','f'],['\\sqrt{}', '','\u221A'],['\\sqrt[]{}', '','\u221B'],
            ['\\alpha ', '','\u03B1'],['\\beta ', '','\u03B2'],['\\gamma ', '','\u03B3'],['\\theta ', '','\u03B8'],['\\omega ', '','\u03C9'],
            ['\left|\\right|','','A'],
            ['\\frac{d}{dx}{}', '','D'],['\\int{ dx}', '','\u222B'],['\\int_{}^{}{ dx}', '','d'],
            ['\\sum_{k=1}^{n}{}', '','\u2211'],['\\lim_{x\\to }{}', '','m'],['\\infty ', '','\u221E'],
            ['\\sin{}', '','s'],['\\cos{}', '','c'],['\\tan{}', '','t'],['\\log{}', '','g'],['_{}\\P_{}', '','P'],['_{}\\C_{}', '','C']]    
    
def cnfont(size):
    font = QtGui.QFont('Consolas', size, QtGui.QFont.Normal)
    return font
    
    
fontSizes = ['6','7','8','9','10','11','12','14','16','18','20','22','24','26','28','32','36']  
DEFAULT_FONT_SIZE_POS = 3
default_font = cnfont(int(fontSizes[DEFAULT_FONT_SIZE_POS]))
#print(default_font. pointSize())
TAB_WIDGET_NUM = 20        
        
DEFAULT_LATEX_FONT_SIZE_INDEX = 4

class TableWidgetDragRows(QtGui.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TableWidgetDragRows, self).__init__(*args, **kwargs)
        
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        

    def mousePressEvent(self, event):
        try:            
            self.from_row = self.itemAt(event.pos()).row()
            super().mousePressEvent(event)
        except:
            pass
        

    def dropEvent(self, event):
        if not event.isAccepted() and event.source() == self:
            tw_list =tw_items_list(self)
            drop_row = self.drop_on(event)            
            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = \
                [[QtGui.QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                    for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1
            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            if drop_row != self.from_row:
                command = TableWidgetCommand(self, tw_list, "drag rows")
                self.parent.parent.undo_stack.push(command)
                self.parent.parent.set_state_reundo_button()
            event.accept()            
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)            
        super().dropEvent(event)   
        

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()
        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()
        

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & QtCore.Qt.ItemIsDropEnabled) \
                and pos.y() >= rect.center().y()
                


def tw_items_list(tw):
    _tw = tw
    i_list = []
    for row in range(_tw.rowCount()):
        i_list.append([_tw.item(row,0).text(), _tw.item(row,1).text(), _tw.item(row,2).text()])
    return i_list   
    
    

def set_tw_items_list(tw, tw_list):
    row_count=tw.rowCount()
    for row in range(row_count):
                tw.removeRow(row_count - row - 1)  
    for row in range(len(tw_list)):
        tw.insertRow(row)
        tw.setItem(row,0,QtGui.QTableWidgetItem(tw_list[row][0]))
        tw.setItem(row,1,QtGui.QTableWidgetItem(tw_list[row][1]))
        tw.setItem(row,2,QtGui.QTableWidgetItem(tw_list[row][2]))
        


class TableWidgetCommand(QtGui.QUndoCommand):
    def __init__(self, tw, init_tw_list, description):
        QtGui.QUndoCommand.__init__(self, description)
        self._tw = tw
        self._init_tw_list = init_tw_list
        self.current_tw_list = tw_items_list(tw)
        self.description = description    
        
            
    def undo(self):
        set_tw_items_list(self._tw, self._init_tw_list )
        self._tw.parent.setCurrentIndex(self._tw.parent.indexOf(self._tw))
        

    def redo(self):
        set_tw_items_list(self._tw, self.current_tw_list )   
        self._tw.parent.setCurrentIndex(self._tw.parent.indexOf(self._tw))
        
 
clip_row = []

class LaTeXExprTableWidget(TableWidgetDragRows):  
    #keyPressSignal = QtCore.Signal() #PySide
    keyPressSignal = QtCore.pyqtSignal() #PyQt4
    def __init__(self, rows=0, columns=3, parent=None):  
        super(LaTeXExprTableWidget, self).__init__(rows, columns, parent)         
        self.parent = parent
        
        self.itemChanged.connect(self.on_item_changed)
        
        #display menu right click
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)        
        self.customContextMenuRequested.connect(self.rightClickMenu)
        
        
        HHIs=['Input(LaTeX Expression)','Calculation','Output(LaTeX Expression)']
        HHIs_width=[800,180,800]
        for column in range(3):
            hitem = QtGui.QTableWidgetItem()
            hitem.setText(HHIs[column])
            hitem.setTextAlignment(QtCore.Qt.AlignLeft)
            self.setHorizontalHeaderItem(column, hitem)
            self.setColumnWidth(column, HHIs_width[column])
        self.selectrow=0
        stylesheet = "::section{Background-color:gray}"
        self.horizontalHeader().setStyleSheet(stylesheet)
        self.verticalHeader().setStyleSheet(stylesheet)

        
    def  on_item_changed(self):
        self.parent.parent.modified = True
                
            
    def rightClickMenu(self,pos):
        rowCount=self.rowCount()
        Menu  = QtGui.QMenu(self)
        if rowCount == 0 and clip_row != []:            
            AppendRow = QtGui.QAction("append copied or cut row to the sheet",self,triggered=self.append_row)
            Menu.addAction(AppendRow)
            Menu.exec_(self.mapToGlobal(pos))
        else:        
            try:                
                indexAt=self.indexAt(pos)
                self.row=indexAt.row()
                self.col=indexAt.column()
                text0=self.item(self.row,0).text()
                copy_str = text0
                if len(text0) > 10:
                    copy_str = text0[:10]+'...'
                copyRow = QtGui.QAction("copy this {:d}th row: {:s}".format(self.row+1, copy_str),self,triggered=self.copyRow)        
                Menu.addAction(copyRow)
                cutRow = QtGui.QAction("cut this {:d}th row: {:s}".format(self.row+1, copy_str),self,triggered=self.cutRow)        
                Menu.addAction(cutRow)
                DeleteRow = QtGui.QAction("remove {:d}th row".format(self.row+1),self,triggered=self.deleteRow)
                Menu.addAction(DeleteRow)
                RemoveAllItems   = QtGui.QAction("remove this Sheet",self,triggered=self.item_all_clear)
                Menu.addAction(RemoveAllItems)
                if clip_row != []:                
                    InsertRow = QtGui.QAction("insert copied or cut row in {:d}th row".format(self.row+1),self,triggered=self.insert_row)
                    Menu.addAction(InsertRow)
                    AppendRow = QtGui.QAction("append copied or cut row to the end of sheet",self,triggered=self.append_row)
                    Menu.addAction(AppendRow)
                Menu.exec_(self.mapToGlobal(pos))
            except:
                pass       
    

    def append_row(self):
        tw_list =tw_items_list(self)
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row,0,QtGui.QTableWidgetItem(clip_row[0]))
        self.setItem(row,1,QtGui.QTableWidgetItem(clip_row[1]))
        self.setItem(row,2,QtGui.QTableWidgetItem(clip_row[2])) 
        command = TableWidgetCommand(self, tw_list, 'append row')
        self.parent.parent.undo_stack.push(command)
        self.parent.parent.set_state_reundo_button()
        self.setCurrentCell(row, 0)
                
     
    def insert_row(self):
        tw_list =tw_items_list(self)
        row = self.row
        self.insertRow(row)
        self.setItem(row,0,QtGui.QTableWidgetItem(clip_row[0]))
        self.setItem(row,1,QtGui.QTableWidgetItem(clip_row[1]))
        self.setItem(row,2,QtGui.QTableWidgetItem(clip_row[2])) 
        command = TableWidgetCommand(self, tw_list, 'insert row')
        self.parent.parent.undo_stack.push(command)
        self.parent.parent.set_state_reundo_button()
        if self.row < self.rowCount():
            self.setCurrentCell(self.row, 0)
        else:
            self.setCurrentCell(self.row-1, 0)  
                
    
    def sheet_text(self):
        copy_lines = ''
        for row in range(self.rowCount()):
            text0=self.item(row,0).text()
            text1=self.item(row,1).text()
            text2=self.item(row,2).text()
            line_str = '$'+text0+'$' + '~--~' + text1 + '$~\\to~$' + '$'+text2+'$' + '\\par\n'
            copy_lines += line_str
        copy_lines = mylatexstyle(copy_lines.replace('&', ' ,~ '))
        return copy_lines        
            
    
    def cutRow(self): 
        tw_list =tw_items_list(self)
        global clip_row
        text0=self.item(self.row,0).text()
        text1=self.item(self.row,1).text()
        text2=self.item(self.row,2).text()
        clip_row = [text0, text1, text2] 
        self.removeRow(self.row)
        command = TableWidgetCommand(self, tw_list, "item all clear")            
        self.parent.parent.undo_stack.push(command)
        self.parent.parent.set_state_reundo_button()
        if self.row < self.rowCount():
            self.setCurrentCell(self.row, 0)
        else:
            self.setCurrentCell(self.row-1, 0)
        
    
    def copyRow(self): 
        global clip_row
        text0=self.item(self.row,0).text()
        text1=self.item(self.row,1).text()
        text2=self.item(self.row,2).text()
        clip_row = [text0, text1, text2]        
        
    
    def deleteRow(self): 
        try:
            tw_list =tw_items_list(self)
            self.removeRow(self.row)
            command = TableWidgetCommand(self, tw_list, 'delete row')
            self.parent.parent.undo_stack.push(command)
            self.parent.parent.set_state_reundo_button()
            if self.row < self.rowCount():
                self.setCurrentCell(self.row, 0)
            else:
                self.setCurrentCell(self.row-1, 0)
            self.parent.parent.modified = True                      
        except:
            pass
            
    
    def item_all_clear(self):
        row_count=self.rowCount()
        if row_count == 0:
            return
        else:
            tw_list =tw_items_list(self)
            for row in range(row_count):
                self.removeRow(row_count - row - 1)            
            command = TableWidgetCommand(self, tw_list, "item all clear")            
            self.parent.parent.undo_stack.push(command)
            self.parent.parent.set_state_reundo_button()
                        
            
    def keyPressEvent(self,event):
        key = event.key()
        if key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_Down:
            super(LaTeXExprTableWidget, self).keyPressEvent(event)
            self.keyPressSignal.emit()
            self.selectRow(self.currentRow())            
    
         
    def mousePressEvent(self,event):    
        super(LaTeXExprTableWidget, self).mousePressEvent(event)
        self.selectRow(self.currentRow())
        
        
    def selectRow(self,row):
        super(LaTeXExprTableWidget, self).selectRow(row)
        self.selectrow = self.currentRow()         
        
        
        
class TabBar(QtGui.QTabBar): # editable tab
    def __init__(self, *args, **kargs):
        super(TabBar, self).__init__(*args, **kargs)    
           
        #self.setMovable(True)
        self._editor = QtGui.QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)            
      
       
    def mouseReleaseEvent (self, event):
        self.setCurrentIndex(self.currentIndex ())
        super(TabBar, self).mouseReleaseEvent(event)       
    
    
    def eventFilter(self, widget, event):
        if ((event.type() == QtCore.QEvent.MouseButtonPress and
             not self._editor.geometry().contains(event.globalPos())) or
            (event.type() == QtCore.QEvent.KeyPress and
             event.key() == QtCore.Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QtGui.QTabBar.eventFilter(self, widget, event)
        

    def mouseDoubleClickEvent(self, event):
        index = self.tabAt(event.pos())         
        if index >= 0:            
            self.editTab(index)
            

    def editTab(self, index):
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()
            self._editor.selectAll()
            

    def handleEditingFinished(self):
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())
                        


class TabTableWidget(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(TabTableWidget, self).__init__(parent) 
        self.setTabBar(TabBar(self))
        self.setMovable(True)        
        
        self.parent = parent        
        for i in range(TAB_WIDGET_NUM):
            self.addTab(LaTeXExprTableWidget(parent=self), 'Sheet{:02d}'.format(i+1))
            
            
    def all_clear(self):
        for i in range(TAB_WIDGET_NUM):
            self.widget(i).item_all_clear()
            self.setTabText(i, 'Sheet{:02d}'.format(i+1))
        self.setCurrentIndex(0)
        


class LaTeXFigureCanvas(FigureCanvas):
    def __init__(self, width=10, height=1, dpi=100, parent=None):        
        self._figure = Figure(figsize=(width, height), facecolor='white', dpi=dpi)
        FigureCanvas.__init__(self, self._figure)        
        self._size = 1
        
        
    def update_figure(self, text):
        self._figure.suptitle(text, x=0.005, y=0.970, horizontalalignment='left',verticalalignment='top' ,size=self._size)
        self.draw()
        
        
    def set_size_index(self, _size):
        self._size = _size
        
        
        
append_replace_mode = ['','append','insert','replace']

view_mode=['view mode OFF', 'view mode ON']
VIEW_MODE_ON = 1
VIEW_MODE_OFF = 0


MATH_FORM_BUTTON_WIDTH=25

class MathFormButton(QtGui.QToolButton):
    #easyButtonSignal = QtCore.Signal(str) #PySide
    easyButtonSignal = QtCore.pyqtSignal(str) #PyQt4
    def __init__(self, tex_text, png_image, text, parent=None):
        super(MathFormButton, self).__init__(parent) 
        self.tex_text = tex_text
        _icon=QtGui.QIcon()
        _icon.addPixmap(QtGui.QPixmap(png_image))
        self.setIcon(_icon)
        self.setText(text)
        self.setFixedWidth(MATH_FORM_BUTTON_WIDTH)
        self.setToolTip(tex_text)
        self.setFont(default_font)
       

    def mousePressEvent(self, event):
        super(MathFormButton, self).mousePressEvent(event)
        self.easyButtonSignal[str].emit(self.tex_text)
        
        
        
def comp_square_x(expr):
    expr_degree=degree(expr, gen=x)
    if expr_degree != 2:
        raize
    ans = solve(Eq(diff(expr, x), 0),x)
    p=ans[0]    
    q=simplify(expr.subs(x, p))
    a=diff(expr, x, 2).subs(x, 0)/2 
    return a*(x-p)**2+q   
        
        
 
class NonEditableQLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(NonEditableQLineEdit, self).__init__(parent)
        
    def keyPressEvent(self,event):
        key = event.key()
        if key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_Right \
            or key == QtCore.Qt.Key_End or key == QtCore.Qt.Key_Home:
            super(NonEditableQLineEdit, self).keyPressEvent(event)
            


class InputLineEditCommand(QtGui.QUndoCommand):
    def __init__(self, line_edit, init_text, description):
        QtGui.QUndoCommand.__init__(self, description)
        self._line_edit = line_edit
        self._current_text = line_edit.text()
        self._init_text = init_text

       
    def undo(self):
        self._line_edit.setText(self._init_text)
        self._line_edit.init_text = self._line_edit.text()
        self._line_edit.setFocus(QtCore.Qt.OtherFocusReason)
        

    def redo(self):
        self._line_edit.setText(self._current_text)
        self._line_edit.init_text = self._line_edit.text()
        self._line_edit.setFocus(QtCore.Qt.OtherFocusReason)
        

 
class InputLineEdit(QtGui.QLineEdit):            
    def __init__(self, parent):
        super(InputLineEdit, self).__init__(parent)
        self.parent = parent
        self.init_text = self.text()
        
        
    def focusInEvent(self, event):        
        self.init_text = self.text()
        self.parent.myparent.undo_button.setEnabled(True)
        QtGui.QLineEdit.focusInEvent(self, event)
    
    
    def focusOutEvent(self, event):
        if self.text() != self.init_text:            
            command = InputLineEditCommand(self, self.init_text, "editing input")
            self.parent.undo_stack.push(command)
            self.parent.set_state_reundo_button()
        QtGui.QLineEdit.focusOutEvent(self, event)
        
        
    def mousePressEvent(self, event):  
        self.setFocus()
        super(InputLineEdit, self).mousePressEvent(event)
        

  


class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent) 
        
        self.myparent = None
        
        self.undo_stack = QtGui.QUndoStack()
        self.tab =TabTableWidget(self) 
        self.modified = False 
                
        self.calculation = 'simplify'
        self.viewmode = VIEW_MODE_OFF
        
        self.inputlabel=QtGui.QLabel('<font color=white>Input(LaTeX Expression)  ')
        self.outputlabel=QtGui.QLabel('<font color=white>Output(LaTeX Expression)  ')
        self.calculation_label=QtGui.QLabel('<font color=white>Calculation')
        self.ltw_label=QtGui.QLabel('<font color=white>LaTeX Expression Table')
        self.tablename_label=QtGui.QLabel('<font color=white>Name:')
        
        self.input_edit = InputLineEdit(self)
        self.input_edit.setFont(cnfont(10))
        self.input_edit.setFocus()
        self.input_clear_button= QtGui.QToolButton()
        self.input_clear_button.setIcon(QtGui.QIcon('./images/delete.ico'))
        
        self.calculation_list=QtGui.QListWidget(self)
        self.calculation_list.setFixedWidth(CALCULATION_LIST_WIDTH)
        for i in range(len(CALCULATION_LIST)):
            self.calculation_list.addItem(CALCULATION_LIST[i])
        self.calculation_list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        
        self.output_edit = NonEditableQLineEdit()
        self.output_edit.setFont(cnfont(10))
        self.output_edit.setReadOnly(True)
        self.output_latex_canvas = LaTeXFigureCanvas()
        self.input_latex_canvas = LaTeXFigureCanvas() 

        down_icon=QtGui.QIcon('./images/down.ico')                
        self.down_combobox=QtGui.QComboBox()
        self.down_combobox.addItem(down_icon, append_replace_mode[0])
        self.down_combobox.addItem(append_replace_mode[1])
        self.down_combobox.addItem(append_replace_mode[2])
        self.down_combobox.addItem(append_replace_mode[3])
        
        self.down_button= QtGui.QToolButton()        
        self.down_button.setIcon(down_icon)
        
        self.up_button= QtGui.QToolButton()
        self.up_button.setIcon(QtGui.QIcon('./images/up.ico'))
        self.up_button.setEnabled(True)   
        
        
        self.math_form_button_list = []
        for el in math_form_list:
            element =MathFormButton(el[0], './images/{:s}'.format(el[1]), el[2])
            self.math_form_button_list.append(element)        
        
        layouth1 = QtGui.QHBoxLayout() 
        layouth1.setSpacing(0)
        layouth1.addSpacing(10)
        layouth1.addWidget(self.inputlabel,alignment=(QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom))
        layouth1.addWidget(self.input_clear_button)
        layouth1.addSpacing(10)        
        for i in range(len(math_form_list)):            
            layouth1.addWidget(self.math_form_button_list[i])
        layouth1.addStretch(1)
        
        layouth2 = QtGui.QHBoxLayout() 
        layouth2.addWidget(self.outputlabel,alignment=(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop))
        layouth2.addStretch(1)
        
        layoutv1 = QtGui.QVBoxLayout()        
        layoutv1.addLayout(layouth1)
        layoutv1.addWidget(self.input_edit)
        layoutv1.addWidget(self.input_latex_canvas )
        layoutv1.addLayout(layouth2)
        layoutv1.addWidget(self.output_edit)
        layoutv1.addWidget(self.output_latex_canvas )        
        
        layoutv2 = QtGui.QVBoxLayout()  
        layoutv2.addWidget(self.calculation_label,alignment=(QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom))
        layoutv2.addWidget(self.calculation_list)
        
        layouth3 = QtGui.QHBoxLayout()
        layouth3.addLayout(layoutv1)
        layouth3.addLayout(layoutv2)

        layouth4 = QtGui.QHBoxLayout()
        layouth4.addWidget(self.ltw_label,alignment=(QtCore.Qt.AlignBottom))
        layouth4.addWidget(self.tablename_label,alignment=(QtCore.Qt.AlignBottom))
        layouth4.addStretch(1)
        layouth4.addWidget(self.up_button,alignment=QtCore.Qt.AlignCenter)
        layouth4.addStretch(1)
        layouth4.addWidget(self.down_combobox)
        layouth4.addStretch(1)        
               
        layout = QtGui.QVBoxLayout()  
        layout.addLayout(layouth3,stretch = 0)
        layout.addLayout(layouth4,stretch = 0)
        layout.addWidget(self.tab)
        self.setLayout(layout)             

        self.input_edit.returnPressed.connect(self.updateCanvas)        
        self.input_clear_button.clicked.connect(self.input_edit_clear)
        self.calculation_list.itemClicked.connect(self.updateCanvas)
        self.up_button.clicked.connect(self.table_to_io)
        self.calculation_list.currentRowChanged[int].connect(self.cl_row_updateCanvas)
        for i in range(len(math_form_list)):
            self.math_form_button_list[i].easyButtonSignal[str].connect(self.math_form_insert)        
        self.down_combobox.activated[str].connect(self.down_combobox_action)
        for i in range(TAB_WIDGET_NUM):
            self.tab.widget(i).clicked.connect(self.table_to_io_vm)
            self.tab.widget(i).keyPressSignal.connect(self.table_to_io_vm)        
        
        
    def set_state_reundo_button(self):
        if self.undo_stack.index() > 0:
            self.myparent.undo_button.setEnabled(True)
        else:
            self.myparent.undo_button.setEnabled(False)
        if self.undo_stack.index() < self.undo_stack.count():
            self.myparent.redo_button.setEnabled(True)
        else:
            self.myparent.redo_button.setEnabled(False)
    
    def set_myparent(self, p):
        self.myparent = p
        

    #@QtCore.Slot(str) #PySide
    @QtCore.pyqtSlot(str) #PyQt4
    def math_form_insert(self, tex_text):       
        if self.input_edit.hasFocus():
            self.input_edit.insert(tex_text)
    
    def input_edit_clear(self):
        self.input_edit.setFocus()
        self.input_edit.clear()
        self.input_edit.setFocus()
        self.updateCanvas()
        
        
    def copy_io(self):        
        text0=self.input_edit.text()
        text1=CALCULATION_LIST[self.calculation_list.currentRow()]
        text2=self.output_edit.text()
        copy_text = '$'+text0+'$' + ' --- ' + text1 + ' --- ' + '$'+text2+'$'
        copy_text = mylatexstyle(copy_text.replace('&', ' ,~ '))
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(copy_text, mode=cb.Clipboard)
        
        
    def cl_row_updateCanvas(self, row):        
        self.calculation= CALCULATION_LIST[row]
        if self.calculation_list.hasFocus():
            self.updateCanvas()
    
    
    def down_combobox_action(self,text):
        self.down_combobox.setCurrentIndex(0) 
        tw=self.tab.currentWidget()
        tw_list =tw_items_list(tw)
        if text == '':
            return
        if text == 'append':
            row = tw.rowCount()
            result = QtGui.QMessageBox.question(self, 'Question', 
                'Do you append\n this input expression \n to the end of sheet?'.format(row+1),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.No:                
                return             
            tw.insertRow(row)            
        elif text == 'replace':
            row = tw.currentRow()
            if row == -1:
                result = QtGui.QMessageBox.warning(self, 'Warning', 'You can\'t replace!')
                return
            result = QtGui.QMessageBox.question(self, 'Question', 
                'Do you replace\n this input expression with\n {:d}th row expression?'.format(row+1),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.No:                
                return            
        elif text == 'insert':
            row = tw.currentRow()
            if row == -1:
                result = QtGui.QMessageBox.warning(self, 'Warning', 'You can\'t insert!')
                return
            result = QtGui.QMessageBox.question(self, 'Question', 
                'Do you insert \n this input expression with\n {:d}th row expression?'.format(row+1),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.Yes:                
                tw.insertRow(row)
            else:
                return          
        tw.setItem(row,0,QtGui.QTableWidgetItem(self.input_edit.text()))
        tw.setItem(row,1,QtGui.QTableWidgetItem(CALCULATION_LIST[self.calculation_list.currentRow()]))
        tw.setItem(row,2,QtGui.QTableWidgetItem(self.output_edit.text()))        
        command = TableWidgetCommand(tw, tw_list, "down action")            
        self.undo_stack.push(command)
        self.set_state_reundo_button()
        tw.setCurrentCell(row,0)

            
    def setViewmode(self,text):
        if text == 'view mode ON':
            self.viewmode = VIEW_MODE_ON
            self.up_button.setEnabled(False)
        elif text == 'view mode OFF':
            self.viewmode = VIEW_MODE_OFF
            self.up_button.setEnabled(True)
            
            
    def new(self):
        if self.maybeSave():
            self.input_edit.clear()
            self.output_edit.clear()
            self.calculation_list.setCurrentRow(0)
            self.updateCanvas()
            self.currentFilename ='New'
            self.setTableTitle(self.currentFilename)
            self.tab.all_clear()
            self.undo_stack.clear()
            self.set_state_reundo_button()
            self.input_edit.setFocus()
            self.modified = False      
    

    def saveAs(self):
        #fileName, filtr = QtGui.QFileDialog.getSaveFileName(self, 'save as file', dir='./data', filter='ls_calc data files (*.lsc)') #PySide
        fileName= QtGui.QFileDialog.getSaveFileName(self, 'save as file', './data', 'ls_calc data files (*.lsc)') #PyQt4
        if fileName:
            self.setTableTitle(fileName)
            self.currentFilename =fileName
            return self.savefile(fileName) 
        return False
            
            
    def save(self):
        if self.currentFilename != '' and self.currentFilename != 'New':
            return self.savefile(self.currentFilename)
        return self.saveAs() 
        
        
    def savefile(self,filename): 
        try:
            save_data=''
            for i in range(TAB_WIDGET_NUM):
                save_data += self.tab.tabText(i)+'$$'
            save_data += '%\n'  
            for i in range(TAB_WIDGET_NUM):
                save_data += 'Sheet{:02d}\n'.format(i+1)
                tw=self.tab.widget(i)
                for row in range(tw.rowCount()):
                    save_data += tw.item(row,0).text()+'#--#'
                    save_data += tw.item(row,1).text()+'#--#'
                    save_data += tw.item(row,2).text() +'%\n'
                save_data += '%\n'
            f = open(filename, 'w') 
            f.write(save_data)
            f.close()
            self.modified = False
            return True
        except:
            print('save error')
            return False
        
    
    def setTableTitle(self, filename):
        if filename != '':
            f1=filename.rsplit("/", 1)[-1]
            f_name=f1.rsplit('.')[0]
        else:
            f_name='New'
        title_name =': '+f_name
        self.tablename_label.setText('<font color=white>'+title_name)
        
        
    def open(self):
        if self.maybeSave():
            #fileName,filtr = QtGui.QFileDialog.getOpenFileName(self, 'open file', dir='./data', filter='ls_calc data files (*.lsc)') #PySide
            fileName  = QtGui.QFileDialog.getOpenFileName(self, 'open file','./data',"ls_calc data files (*.lsc)") #PyQt4
            if fileName:
                self.loadfile(fileName) 
            
               
    def loadfile(self,filename):
        try:
            f = open(filename, 'r')        
            load_data = str(f.read())
            self.currentFilename = filename
            self.tab.all_clear()
            load_data1 = re.split('\$\$\%\n', load_data)
            tab_title_list=re.split('\$\$', load_data1[0])
            table_widget_list =[]
            tw_lists=re.split(r'Sheet\d\d', load_data1[1])
            for i in range(TAB_WIDGET_NUM):
                tw_list=re.split(r'\%\n',tw_lists[i+1])
                if tw_list == ['\n', '']:
                    table_widget_list.append([])
                else:
                    row_list = []
                    for le in tw_list:                    
                        if le != '':
                            le_list1= re.split(r'\#--\#',le)
                            le_list = []
                            for element in le_list1:
                                le_list.append(element.replace('\n',''))
                            row_list.append(le_list)
                    table_widget_list.append(row_list)
            for i in range(TAB_WIDGET_NUM):
                self.tab.setTabText(i,tab_title_list[i])
                tw_list = table_widget_list[i]
                for row in range(len(tw_list)):
                    self.tab.widget(i).insertRow(row)
                    self.tab.widget(i).setItem(row,0,QtGui.QTableWidgetItem(tw_list[row][0]))
                    self.tab.widget(i).setItem(row,1,QtGui.QTableWidgetItem(tw_list[row][1]))
                    self.tab.widget(i).setItem(row,2,QtGui.QTableWidgetItem(tw_list[row][2]))
            self.tab.widget(0).setCurrentCell(0,0)
            self.table_to_io()
            f.close()            
            self.setTableTitle(filename)
            self.undo_stack.clear()
            self.set_state_reundo_button()
            self.modified = False      
        except:
            print('file load error!')    
     
    def copy_to_clipboard(self):
        copy_lines =''
        for i in range(TAB_WIDGET_NUM):
            tw=self.tab.widget(i)
            if tw.rowCount() != 0:
                copy_lines += self.tab.tabText(i) + '\\par\n' + tw.sheet_text() + '\\par\n'
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(copy_lines, mode=cb.Clipboard) 
    
    
    def mylatexstyle2(self, texexpr):
        replace_list=[['~','\;\, '], ['\\{','('],['\\}', ')'],
            ['\\dfrac','\\frac'],['\\C','\\mathrm{C}'],['\\P','\\mathrm{P}'],
            ['\\ii',' i'],['\\ee',' e'],['\\ppi','\\pi '],['\\dfrac','\\frac'],['&',', \quad ']]
        for le in replace_list:
            texexpr=texexpr.replace(le[0],le[1]) 
        return texexpr        

    
    def item_click(self, item):
        try:
            self.calculation=item.text()
            self.updateCanvas()
        except:
            self.input_latex_canvas.update_figure('None')            
            self.output_latex_canvas.update_figure('None')
            
            
    def io_to_table_append(self):
        tw=self.tab.currentWidget()
        row = tw.rowCount()
        tw.insertRow(row)
        tw.setItem(row,0,QtGui.QTableWidgetItem(self.input_edit.text()))
        tw.setItem(row,1,QtGui.QTableWidgetItem(CALCULATION_LIST[self.calculation_list.currentRow()]))
        tw.setItem(row,2,QtGui.QTableWidgetItem(self.output_edit.text()))        
            

    def table_to_io(self):
        try:      
            tw=self.tab.currentWidget()
            row = tw.currentIndex().row()
            input_texexpr= tw.item(row,0).text()
            output_texexpr= tw.item(row,2).text()
            self.input_edit.setText(input_texexpr)
            self.calculation_list.setCurrentRow(calculation_dict[tw.item(row,1).text()])
            self.calculation=tw.item(row,1).text()
            self.output_edit.setText(output_texexpr)
            self.input_latex_canvas.update_figure(r'$'+self.mylatexstyle2(input_texexpr)+'$')
            self.output_latex_canvas.update_figure(r'$'+output_texexpr+'$')
        except:
            pass    
    
    
    def table_to_io_vm(self):
        if self.viewmode == VIEW_MODE_OFF:
            return
        else:
            self.table_to_io()     
        
    
    def updateCanvas(self):
        try:
            texexpr = self.input_edit.text()
            if self.calculation=='simplify':
                result_texexpr = mylatex(simplify(tex2sym(texexpr)))
            elif self.calculation=='factor':
                result_texexpr = mylatex(factor(tex2sym(texexpr)))
            elif self.calculation=='expand':
                result_texexpr = mylatex(expand(tex2sym(texexpr)))
            elif self.calculation=='rationalize-denom':
                result_texexpr = mylatex(radsimp(simplify(tex2sym(texexpr))))
            elif self.calculation=='sqrtdenest':
                result_texexpr = mylatex(sqrtdenest(tex2sym(texexpr)))
            elif self.calculation=='nsimplify':
                result_texexpr = mylatex(nsimplify(tex2sym(texexpr)))
            elif self.calculation=='equation-x': 
                texexpr_list = re.split('&', texexpr)
                if len(texexpr_list) != 1:
                    raise
                eq=expand(tex2sym(texexpr))
                result_texexpr = mylatex(solve([eq.lhs - eq.rhs] ,[x], domain=S.Complexes ))
            elif self.calculation=='equation-xy': 
                texexpr_list = re.split('&', texexpr)
                if len(texexpr_list) != 2:
                    raise
                eq1=expand(tex2sym(texexpr_list[0]))
                eq2=expand(tex2sym(texexpr_list[1]))
                result_texexpr = mylatex(solve([eq1.lhs - eq1.rhs, eq2.lhs - eq2.rhs] ,[x,y], domain=S.Complexes ))
            elif self.calculation=='equation-xyz':                 
                texexpr_list = re.split('&', texexpr)
                if len(texexpr_list) != 3:
                    raise
                eq1=expand(tex2sym(texexpr_list[0]))
                eq2=expand(tex2sym(texexpr_list[1]))
                eq3=expand(tex2sym(texexpr_list[2]))
                result_texexpr = mylatex(solve([eq1.lhs - eq1.rhs, eq2.lhs - eq2.rhs, eq3.lhs - eq3.rhs] ,[x,y,z], 
                        domain=S.Complexes ))
            elif self.calculation=='inequality-x-1':
                result_texexpr = mylatex(solve_univariate_inequality(simplify(tex2sym(texexpr)), x, relational=False))
            elif self.calculation=='inequality-x-2':
                texexpr_list = re.split('&', texexpr)
                leq1=expand(tex2sym(texexpr_list[0]))
                leq2=expand(tex2sym(texexpr_list[1]))
                result_set1=solve_univariate_inequality(simplify(leq1), x, relational=False)
                result_set2=solve_univariate_inequality(simplify(leq2), x, relational=False)               
                result_texexpr = mylatex(Intersection(result_set1,result_set2))
            elif self.calculation=='recursive-form-1':                
                texexpr_list = re.split('&', texexpr)
                if len(texexpr_list) != 2:
                    raise
                eq=expand(tex2sym(texexpr_list[0]))
                a1=expand(tex2sym((texexpr_list[1]).replace('a_1=','')))
                result_texexpr = mylatex(rsolve(eq,F(n), {F(1):a1}))
                result_texexpr = 'a_n='+result_texexpr
            elif self.calculation=='recursive-form-2':
                texexpr_list = re.split('&', texexpr)
                if len(texexpr_list) != 3:
                    raise
                eq=expand(tex2sym(texexpr_list[0]))
                a1=expand(tex2sym((texexpr_list[1]).replace('a_1=','')))
                a2=expand(tex2sym((texexpr_list[2]).replace('a_2=','')))
                result_texexpr = mylatex(rsolve(eq,F(n), {F(1):a1,F(2):a2}))
                result_texexpr = 'a_n='+result_texexpr
            elif self.calculation=='diff-equation-f(x)':
                result_texexpr = mylatex(dsolve(simplify(tex2sym(texexpr)),f(x)))
            elif self.calculation=='convert-to-decimal':
                result_texexpr = mylatex((simplify(tex2sym(texexpr))).evalf())  
            elif self.calculation=='simplify-power':
                result_texexpr = mylatex(powsimp(tex2sym(texexpr),force=True))
            elif self.calculation=='expand-log':
                result_texexpr = mylatex(expand_log(tex2sym(texexpr),force=True))
            elif self.calculation=='expand-trig':
                result_texexpr = mylatex(expand_trig(tex2sym(texexpr)))
            elif self.calculation=='complete-square-x':
                result_texexpr = mylatex(comp_square_x(simplify(tex2sym(texexpr))))                 
                
            self.output_edit.clear()            
            self.output_edit.setText("{:s}".format(result_texexpr))
            self.output_edit.setCursorPosition(0)
            self.input_latex_canvas.update_figure(r'$'+self.mylatexstyle2(texexpr)+'$')
            self.output_latex_canvas.update_figure(r'$'+result_texexpr+'$')              
            
        except:
            self.output_edit.clear()
            self.output_edit.setText('None')   
            self.input_latex_canvas.update_figure('None')            
            self.output_latex_canvas.update_figure('None')  
            
            
    def maybeSave(self):
        if self.modified == True:
            ret = QtGui.QMessageBox.question(self, "Question","Do you want to save\nthis LaTeX Expression Table?", 
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No| QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel) 
            if ret == QtGui.QMessageBox.Yes:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True
   
            
help_text='<font color=black face="Courier New" size=3><p>\
    <b>"LaTeX SymPy Calculator" is a calculator<br> with LaTeX expression Form by using SymPy.</b><br><br>\
    <b>Input Code</b><br>\
    <b>variable:</b><br>\
    &nbsp;&nbsp;&nbsp;a,b,...,z,A,B,..,Z(exc. E,I,N,O,S)<br>\
    &nbsp;&nbsp;&nbsp;\\alpha,...,\omega(exc. zeta,omicron) <br>\
    <b>math constant:</b><br>\
    &nbsp;&nbsp;&nbsp;&pi; --> \\ppi, i --> \\ii, e --> \\ee<br>\
    <b>LaTeX Code Style:</b><br>\
    &nbsp;&nbsp;&nbsp;\\sin{x},  \\log\_{2}{8},<br>\
    &nbsp;&nbsp;&nbsp;\\sum\_{k=1}\^{n}{k(k+1)\^2},... <br>\
    <b> space :</b><br>\
    &nbsp;&nbsp;&nbsp;\\!&nbsp;   \\,&nbsp;   \\:&nbsp;   \\;&nbsp;   ~ <br><br>\
    Author: <a href="https://github.com/AkiraHakuta/antlr4_tex2sym">Akira Hakuta</a>, Date: 2019/03/30 <br>\
    '      
    



class MainFrame(QtGui.QWidget):
    def __init__(self):
        super(MainFrame, self).__init__()
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.darkBlue)
        self.setPalette(p)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(SLC_TITLE)
        self.setWindowIcon(QtGui.QIcon('ls_calc.ico'))
        self.resize(MAINFRAME_WIDTH, MAINFRAME_HIGHT)
        
        self.form=Form()
        self.form.set_myparent(self)
        
        
        new_action = QtGui.QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.form.new)
        openfile_action = QtGui.QAction('Open', self)
        openfile_action.setShortcut('Ctrl+O')
        openfile_action.triggered.connect(self.form.open)
        savefile_action = QtGui.QAction('Save', self)
        savefile_action.setShortcut('Ctrl+S')
        savefile_action.triggered.connect(self.form.save)
        saveasfile_action = QtGui.QAction('saveAs', self)
        saveasfile_action.setShortcut('Ctrl+A')
        saveasfile_action.triggered.connect(self.form.saveAs)
        copy_to_clipboard_action = QtGui.QAction('copy clip', self)#.
        copy_to_clipboard_action.setShortcut('Ctrl+C') 
        copy_to_clipboard_action.setToolTip('copy LaTeX Expression Table to clipboard')
        copy_to_clipboard_action.triggered.connect(self.form.copy_to_clipboard)
        
        quit_action = QtGui.QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        
        file_menu = QtGui.QMenu(self)        
        file_menu.addAction(new_action)
        file_menu.addAction(openfile_action)
        file_menu.addAction(savefile_action)
        file_menu.addAction(saveasfile_action)
        file_menu.addAction(copy_to_clipboard_action)  
        file_menu.addAction(quit_action)        
        self.connect(file_menu, QtCore.SIGNAL("hovered(QAction *)"), self._actionHovered)
        
        self.fileButton = QtGui.QPushButton('File') 
        self.fileButton.setShortcut('Ctrl+F')        
        self.fileButton.setMaximumWidth(100)        
        self.fileButton.setMenu(file_menu)
        self.fileButton.menu()
        
        self.copy_io_clip_button= QtGui.QToolButton()
        self.copy_io_clip_button.setToolTip('copy Input Output LaTeX Expression to clipboard')
        self.copy_io_clip_button.setIcon(QtGui.QIcon('./images/copy.ico'))
        self.copy_io_clip_button.clicked.connect(self.form.copy_io)    
        
        #redo undo        
        self.undo_button= QtGui.QToolButton()
        self.undo_button.setToolTip('undo')
        self.undo_button.setIcon(QtGui.QIcon('./images/undo.ico')) 
        self.redo_button= QtGui.QToolButton()
        self.redo_button.setToolTip('redo')
        self.redo_button.setIcon(QtGui.QIcon('./images/redo.ico')) 
        self.undo_counter = QtGui.QLineEdit()
        self.undo_counter.setReadOnly(True)
        self.changeUndoCount(0)
        self.form.set_state_reundo_button()
        self.undo_counter.setFixedWidth(105)
        self.undo_button.clicked.connect(self.click_undo)
        self.redo_button.clicked.connect(self.click_redo)
        self.form.undo_stack.indexChanged.connect(self.changeUndoCount)    
        
        self.viewmode_comboBox=QtGui.QComboBox()
        self.viewmode_comboBox.addItems(view_mode)
        
        self.font_size_label=QtGui.QLabel('<font color=white>LaTeX View Font Size:')
        self.font_size_combobox = QtGui.QComboBox()
        self.font_size_combobox.addItems(fontSizes)
        self.font_size_combobox.setCurrentIndex(DEFAULT_LATEX_FONT_SIZE_INDEX)
        self.font_size_index(DEFAULT_LATEX_FONT_SIZE_INDEX)
        
        self.aboutButton = QtGui.QPushButton('Help')
        self.aboutButton.setShortcut('Ctrl+H')  
        self.aboutButton.setMaximumWidth(100)
        self.aboutButton.clicked.connect(self.about)
        
        layouth = QtGui.QHBoxLayout()
        layouth.addWidget(self.fileButton)
        layouth.addWidget(self.copy_io_clip_button)
        layouth.addWidget(self.undo_button)
        layouth.addWidget(self.redo_button)
        layouth.setSpacing(10)
        layouth.addWidget(self.viewmode_comboBox)
        layouth.addWidget(self.font_size_label)
        layouth.addWidget(self.font_size_combobox)
        layouth.addWidget(self.aboutButton)
        layouth.addStretch(1)
        layouth.addWidget(QtGui.QLabel('<font color=white>Undo Stack Counter:'))        
        layouth.addWidget(self.undo_counter)        
        
        layoutv = QtGui.QVBoxLayout()
        layoutv.addLayout(layouth)
        layoutv.addWidget(self.form)
        self.setLayout(layoutv) 
        
        self.viewmode_comboBox.activated[str].connect(self.form.setViewmode)
        self.font_size_combobox.currentIndexChanged.connect(self.font_size_index)
        
        DEMO_FILE = './data/DEMO.slc' 
        self.form.currentFilename = DEMO_FILE 
        #self.form.loadfile(DEMO_FILE)            
        self.form.new() 


    def _actionHovered(self, action):
        tip = action.toolTip()
        QtGui.QToolTip.showText(QtGui.QCursor.pos(), tip)
        
    def click_undo(self):
        self.undo_button.setFocus()
        self.form.undo_stack.undo()
        self.form.set_state_reundo_button()
        
        
    def click_redo(self):
        self.redo_button.setFocus()
        self.form.undo_stack.redo()
        self.form.set_state_reundo_button()
        
    
    def changeUndoCount(self, index):
        self.undo_counter.setText("{:03d}/{:03d}".format(index, self.form.undo_stack.count()))
        
    
    def about(self):
        msg=QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, SLC_TITLE, help_text, parent=self)
        msg.exec_()         
    
            
    def closeEvent(self, event):
        if self.form.maybeSave():
            event.accept()
        else:
            event.ignore() 
            

    def font_size_index(self, size_index):
        SCALE=2.3
        size = int(fontSizes[size_index])
        self.form.input_latex_canvas.set_size_index(int(size*SCALE))
        self.form.output_latex_canvas.set_size_index(int(size*SCALE))
        self.form.updateCanvas()
        
 

application = QtGui.QApplication(sys.argv)
application.setFont(default_font)
main_window = MainFrame()
main_window.show()
sys.exit(application.exec_())
